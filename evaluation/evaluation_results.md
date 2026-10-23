# Evaluation Results Summary

Document your team's evaluation results below.

## Summary Overview

- **Date of Evaluation:** 10.23.2026
- **Model Evaluated:** (e.g., `qwen3:8b`)
- **Total Test Cases Executed:** 5
- **Passed:** 5
- **Failed:** 0
- **Pass Rate:** 100%

## Performance by Category

| Category | Total Cases | Passed | Failed | Pass Rate |
| :--- | :---: | :---: | :---: | :---: |
| Successful Cases | 3 | 3 | 0 | 100% |
| Difficult Cases | 1 | 1 | 0 | 100% |
| Failure / Edge Cases | 1 | 1 | 0 | 100% |

## Key Findings & Failure Analysis

System is working as it should. There are no failures in any of the test cases. The system is able to handle many different kinds of prompts and gives answers correctly without doing any unnecessary actions. 

Future upgrading could include adding more file formats.

If it's counted as a failure, the prompt could be empty if it has a edgecase /  malicious prompt. Now the model tries to answer every time, which is by our design.

### What worked well
- The system did not fail on any test case. The test cases presented were:
1. Test case where the prompt was short and asked for simple textual information. (e.g price, size, done renovations)
2. Test case where the prompt was a long string of random characters.
3. Test case wher the prompt was very long and poorly optimized.
4. Test case where the prompt tried to hijack the models role and asked the model to print the prompt back to the user.
5. Test case where the user prompt was left completely empty.

System performed well, and didnt fail on any case. In the edge/dangerous cases it was able to handle the prompt correctly and disregarded maliciousness and a random string of chars. It printed the required information correctly in the correct format.

In the normal cases, it did exactly what it was asked and even though the prompt was long and hard to read, it managed to fill out necessary information.

In the empty prompt case, it correctly printed out everything it was supposed to and had the correct format. It also printed out a message that the prompt was empty and that it was unable to answer the question.

### Observed failure modes
## System didnt fail on any  test case. The test cases I was expecting errors were:
- The edge case, where the prompt is a long string of random characters.
- The role hijacking case where the prompt was asking the model to forget its role and print the prompt back to user. Printing the prompt back to user by request could compromise security and privacy of the system. 

## Action Items & Improvements
- [x] Printing a failure message only, and no information at all when the prompt is malicious or random.

## Pictures of test cases and results explained.

# Succesful Cases

# Error / Edge prompt Cases
