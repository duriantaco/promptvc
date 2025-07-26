# Step 1: Init your repo

```bash
mkdir promptvc-test
cd promptvc-test
promptvc init
```

## You should see this: 

```bash
Created promptvc.yaml
Added promptvc.yaml to .gitignore
Initialized prompt repo at ./.promptvc
```

## Verification:

[] Check that .promptvc/ directory exists
[] Check that promptvc.yaml exists with template configuration
[] Check that .gitignore contains promptvc.yaml

# Step 2: Prompt management

## Create your prompt

```bash
promptvc add summarizer "Summarize this article in 3 sentences or less: {input}"
```

You should see this response `Added/updated prompt 'summarizer' (staged)`

## Commit your prompt

```bash
promptvc commit summarizer "Summarizer prompt"
```

You should see this `Committed prompt 'summarizer' with message: Summarizer prompt`

### If you want you can add multiple versions like so:

```bash
promptvc add summarizer "Provide a concise summary of this article focusing on key points: {input}"
promptvc commit summarizer "Version 2 - more detailed instruction"

promptvc add summarizer "In one paragraph, summarize: {input}"
promptvc commit summarizer "Version 3 - one paragraph format"
```

## History
```bash
promptvc history summarizer
```

You should see these 3 versions below:

```
Version 1: Initial summarizer prompt (2025-07-24T10:30:45.123456)
Version 2: Version 2 - more detailed instruction (2025-07-24T10:31:12.789012)
Version 3: Version 3 - one paragraph format (2025-07-24T10:31:45.345678)
```

# Step 3: Checkout

Run this to checkout your prompt:

```bash
promptvc checkout summarizer 1
```

To checkout a diff version just change the number to whatever version you want:
```bash
promptvc checkout summarizer 2
```

You should see the output of that version

## List all prompts

```bash
promptvc list
```

Now when you run this command, you should see just one output which is `summarizer`

# Step 4: Compare

To compare versions: 

```bash
promptvc diff summarizer 1 2 # or u can change to 1 and 3 instead of 1 and 2
```

# Step 5: Initialize your sample file

The sample file is used to store your inputs

```bash
promptvc init-samples summarizer
```

**Please check** that `summarizer_samples.json` exists with some placeholders. 

## Edit your sample file

```json
[
  {"input": "AI has revolutionized many industries. ML algorithms can now process huge amounts of data to identify patterns and make predictions. Companies are using AI for everything ranging from customer service chatbots to autonomous vehicles. However, there are still a lot of concerns among people, regarding job displacement and privacy"},
  {"input": "Climate change is one of the most pressing issues currently. Rising global temperatures are causing ice caps to melt, sea levels to rise, and weather patterns to become more extreme. Scientists agree that immediate action needs to be taken to reduce greenhouse gas emissions and transition to renewable energy"}
]
```

## Make sure you configure your api keys found inside `promptvc.yaml`

```yaml
llm_providers:
  openai:
    api_key: "your_actual_openai_api_key"
    default_model: "gpt-4-turbo"
  anthropic:
    api_key: "your_actual_anthropic_api_key"
    default_model: "claude-3-sonnet-20240229"
```

# Step 6: Running with openai or anthropic

```bash
promptvc test summarizer 1 2 --llm openai ## or anthropic
```

# Step 7 (more advance stuff) - Create Multiple Prompt Types

```bash
promptvc add translator "Translate the following text to malay: {input}"
promptvc commit translator "Initial malay translator"

promptvc add classifier "Classify this text as positive, negative, or neutral: {input}"
promptvc commit classifier "Sentiment classifier v1"
```

Again, run `promptvc list` and you will see 3 prompt types now. 

Now run the same thing as `step 5`. `promptvc init-samples classifier` but change it from summarizer to classifier now because we're testing the classifier prompt now.


------ THE END FOR CLI -----

# Python API 
```python

from promptvc.repo import PromptRepo
import openai

# step2
def my_llm(prompt):
    client = openai.OpenAI(api_key="your api key(but please put it in .env or something)")
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # or whatever model you prefer
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200,
        temperature=0.7
    )
    
    return response.choices[0].message.content

### step 2
samples = [
    {"input": "AI has revolutionized many industries. ML algorithms can now process huge amounts of data to identify patterns and make predictions. Companies are using AI for everything ranging from customer service chatbots to autonomous vehicles. However, there are still a lot of concerns among people, regarding job displacement and privacy"},
    {"input": "Climate change is one of the most pressing issues currently. Rising global temperatures are causing ice caps to melt, sea levels to rise, and weather patterns to become more extreme. Scientists agree that immediate action needs to be taken to reduce greenhouse gas emissions and transition to renewable energy"},
    {"input": "Remote work has fundamentally changed how companies operate. It offers flexibility and access to global talent. However, it also presents challenges in team collaboration, and employee engagement."}
]

### step3
def main():
    repo = PromptRepo()
        
    ## v1 simple
    repo.add("summarizer", "Summarize this text in 2-3 sentences: {input}")
    repo.commit("summarizer", "v1 - simple summarizer")
    
    ## v2 detailed
    repo.add("summarizer", "Provide a concise summary highlighting the main points: {input}")
    repo.commit("summarizer", "v2 - detailed with challenges")
    
    print("testing both versions")
    results = repo.eval_versions("summarizer", [1, 2], samples, my_llm)
    
    print("----")
    print("compare: ")
    print("-----")
    
    for i, sample in enumerate(samples):
        print(f"\nTest Case {i+1}:")
        print(f"Input: {sample['input'][:100]}...")
        print("-" * 40)
        
        v1_output = results[1]['outputs'][i]['output']
        v2_output = results[2]['outputs'][i]['output']
        
        print(f"Version 1: {v1_output}")
        print(f"Version 2: {v2_output}")
        
        similarity = repo.diff_engine.semantic_diff(v1_output, v2_output)
        print(f"Similarity: {similarity:.2f}")
        print()
    
    v1_avg_length = results[1]['avg_length']
    v2_avg_length = results[2]['avg_length']
    
    print("SUMMARY:")
    
    diff_result = repo.diff("summarizer", 1, 2)
    print(f"Prompt similarity: {diff_result['semantic_similarity']:.2f}")

if __name__ == "__main__":
    main()
```