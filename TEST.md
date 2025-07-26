## CLI

- setup
- teardown
- init command
- init existing configs
- add
- commit
- history
- checkout
- checking out invalid versions (create prompt but dont commit, then try to checkout version 123 which doesnt exist)
- diff  
- list
- init samples
- init samples existing file (accidentally runs promptvc init samples, file should not be lost)
- no samples
- invalid llm (models outside of openai and claude should not accepted yet)
- success
- complete workflow

## Config

- init
- setup
- teardown
- config file not found
- config file is empty
- no llm providers key provided in the config file
- testing valid provider
- loading multiple providers config
- no llm providers value provided in the config file
- extra fields inside the config file
- special characters in value
- numeric values
- malformed yaml file
- null values
- additional sections (like some random data)
- case sensitive for provider names (openai vs OpenAI)

## Diff

- setup
- text diff identical (checking boundary condition where there are 0 differences)
- text diff simple change (instead of `hello world`, become `hello universe`)
- multiline 
- empty string ("", "" should return empty, empty vs 'hello' should return `+ hello`)
-  multi lines (2 lines vs 3 lines, should show new line with the `+`)
- line removal (same as above except now its `-`)
- identical (both words exactly the same)
- similar meaning ('hello world' vs 'hello earth'?)
- opposite meaning
- completely different
- empty strings
- loooong texts
- model loading
- special chars
- test numbers
- whitespaces ('hello world' vs 'hello   world')
- case sensitivity

## LLM
- setup
- teardown
- call openai without a config file
- call openai but never provide openai key and value
- invalid openai api key
- call anthropic without a config file
- call anthropic but never provide anthropic key and value
- invalid anthropic api key
- load different models (e.g. gpt 4 vs claude 3 sonnet)
- test empty config file
- malformed yaml
- missing api key
- missing model

## Pipeline
- init
- default tokens
- setup
- teardown
- single step 
- multiple step 
- non string output 
- trace storage
- save the trace file
- appends to trace file
- feedback valid rating (check the feedback does not exceed 5)
- invalid rating (inputting empty rating)
- skip comment
- rating out of range (inputting rating exceeding 5)
- token counting empty strings

## Repo

- init 
- setup
- teardown
- create directory
- default path
- load versions no file (loading from a non existent file)
- add prompt inside the file (make sure stored correctly)
- adding empty prompt (prevents garbage data)
- add multiple versions (ensure versioning works)
- generating hash
- commit the prompts
- commit no versions fail (trying to commit non existent prompt should fail with error)
- commit allows new version after commit
- history 
- history empty prompt
- history includes uncommitted (should see staged changes)
- checkout
- checking out invalid version (non existent prompt should return `None`)
- diff
- invalid diff version
- without llm
- with llm
- multiple samples (evaluate 3 or more samples)
- invalid versions (non existent version)
- multiple versions (v1 vs v2)
- length ratio
- multiple prompts
- average length calculation
- empty outputs