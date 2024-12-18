question_prompt = """Below is the full XPath of the question object in a HTML page.

'{xpath}'

and following is the HTML content in the given XPath.

{question_section_html}

Just give me the full XPath of the correct option for this question in string format.
your output should contain only the string output which can be loaded into a python variable and executed to click the button directly."""

assessment_prompt = """Below is the full XPath of the question object in a HTML page.

'{xpath}'

and following is the HTML content in the given XPath.

{assessment_section_html}

Just give me the answer text of the correct option for this question in string format just like mentioned below:
'sample answer'
"""