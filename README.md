# TextSummarizer
Takes single documents and extracts most important information for a summary.

Takes text input and prints to console a keyphrase list as well as extracted sentences containing high scoring keyphrases. Replaces text in widget with the summary for evaluation, editing and saving to a file.

Features:
Uses Tkinter text widget for input.
Opens .txt and extracts text from body of .docx documents
Saves text widget contents as .txt
Uses Rapid Automatic Keyword Extraction (RAKE) to score and extract keyphrases from the text, then extracts the sentences where those keyphrases are found to provide a summary.
Supports Copy/Cut/Paste events.

*Attempts to encode all text to 'latin-1' to prevent unicodeExceptions.
