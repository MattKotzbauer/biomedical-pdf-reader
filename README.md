
Update to my fork of the [Biomedical PDF Reader](https://github.com/MattKotzbauer/pdf-reading-tools) using recent changes in OpenAI's API - namely, their fixing of the file-search assistant class cleans up the attaching of the PDF to the assistant.

How to Use: 
1. Run one of the prompt-generating scripts (**getTextPrompts.py**, **getEquationPrompts.py**, **getWordPrompts.py**) on a highlighted PDF. Included in this repo is a highlighted version of Love's DESeq2 paper alongside text\_prompts.txt, the result of running getTextPrompts.py on it
2. Run **pdfDriver.py** with the desired PDF and prompts file as arguments (e.g. python pdfDriver.py Love\_DESeq2.pdf text\_prompts.txt). The answers will then be stored in text\_answers.tex

The current primary question is how to increase the rate at which GPT finds our desired passages, which is likely a matter of getting the prompts right.

An interesting next step for this could be to void the reliance on OpenAI / GPT by running the PDF and prompt interpretation on an open-source model (e.g. [DocFormer](https://arxiv.org/abs/2106.11539)) on cloud spot compute. 

