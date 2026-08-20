### **Test Plan for PDF Summarizer Project**

---

#### **Project Overview**
The **PDF Summarizer** is an application that extracts text from PDF documents and generates summaries using a locally-hosted Large Language Model served via Ollama. The project leverages **LangChain** for the retrieval/summarization pipeline and **Streamlit** for building an interactive UI. The goal of this test plan is to ensure that the application works as expected across various components, including PDF reading, summarization, UI interaction, and error handling.

---

### **1. Objectives**

- Ensure the PDF extraction functionality extracts text from single and multi-page PDFs accurately.
- Validate that the summarization component generates concise and accurate summaries.
- Test the UI for correct file upload functionality.
- Handle error scenarios, such as invalid PDF uploads and an unreachable/unconfigured Ollama server.
- Measure the performance of the system to ensure it processes PDFs and generates summaries in a reasonable time frame.

---

### **2. Scope**

#### **Components to be Tested:**

1. **PDF Reading**
   - Single and multi-page PDF text extraction.
   - Handling of empty or corrupted PDF files.
   
2. **Summarization**
   - Summarizing extracted text accurately and within a defined length.
   - Edge case scenarios, such as handling large text blocks.

3. **User Interface (UI)**
   - File upload functionality in Streamlit.
   - Error handling for invalid file formats in the UI.

4. **Error Handling**
   - Unreachable Ollama server or missing model.
   - Invalid PDF uploads (e.g., non-PDF files).
   
5. **Performance**
   - Time taken to process PDFs and generate summaries.

---

### **3. Test Strategy**

- **Functional Testing**: Verify core functionality like PDF extraction, summarization, and file uploads.
- **Negative Testing**: Test edge cases such as invalid files, an unreachable Ollama server, and empty PDFs.
- **Performance Testing**: Measure response times for text extraction and summarization.
- **UI Testing**: Ensure the Streamlit interface works correctly for file uploads and interaction.
- **Integration Testing**: Verify the flow from PDF extraction to summarization in an integrated manner.

---

### **4. Test Environment**

- **Operating Systems**: Windows 10+, macOS, Linux
- **Python Version**: 3.12 or higher
- **Dependencies**:
  - Streamlit for UI
  - LangChain + langchain-ollama for summarization
  - pypdf for PDF reading
  - sentence-transformers + FAISS for local retrieval
  - Ollama, running locally with a pulled model (default `llama3.2:1b`)
  - pytest for testing
- **Hardware**: General desktop/laptop environments (16 GB RAM, multi-core CPU recommended; more RAM improves local LLM inference speed)

---

### **5. Roles and Responsibilities**

- **Test Manager**: Responsible for defining the test plan, scheduling, and ensuring the tests are executed properly.
- **Test Engineer**: Writing and executing test scripts, reporting issues, and documenting results.
- **Developers**: Fixing bugs identified during testing and improving performance based on test results.

---

### **6. Test Cases**

| Test Case ID  | Test Name                         | Description                                                  | Test Steps                                                                                                                                         | Expected Outcome                               |
|---------------|-----------------------------------|--------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------|
| TC_01         | Single PDF Extraction             | Test if text is extracted from a single PDF                   | 1. Load single PDF. 2. Extract text using `PDFReader.read_pdf()`. 3. Assert extracted text.                                                         | Text should be extracted successfully.         |
| TC_02         | Multi-page PDF Extraction         | Test if text is extracted from all pages in a multi-page PDF  | 1. Load multi-page PDF. 2. Extract text. 3. Check if text from all pages is extracted.                                                              | Text from all pages should be extracted.       |
| TC_03         | Invalid PDF Upload                | Test handling of non-PDF files                                | 1. Try to extract text from a non-PDF file using `PDFReader.read_pdf()`.                                                                            | `PDFExtractionError` should be raised.         |
| TC_04         | Empty PDF Handling                | Test handling of PDFs with no extractable text                | 1. Load a PDF with no text layer. 2. Call `PDFReader.read_pdf()`.                                                                                   | `PDFExtractionError` should be raised.         |
| TC_05         | Summarization Length              | Verify summary is a reasonable length                         | 1. Pass a PDF to `Summarizer.summarize_pdf()`. 2. Assert the summary is non-trivial but bounded.                                                    | Summary should be concise, not excessively long.|
| TC_06         | Summarization Accuracy            | Ensure summary is meaningful                                  | 1. Pass a sample PDF to `Summarizer.summarize_pdf()`. 2. Assert summary is non-empty and relevant to the source text.                               | Summary should make sense contextually.        |
| TC_07         | Ollama Unavailable                | Test unreachable/misconfigured Ollama server handling         | 1. Point `OLLAMA_URL` at an unreachable address. 2. Call `Summarizer.summarize_pdf()`.                                                              | A `SummarizationError` should be raised.       |
| TC_08         | UI File Upload                    | Test file upload via Streamlit UI                             | 1. Upload a PDF via Streamlit UI. 2. Check if the file is processed.                                                                                | File should upload successfully.               |
| TC_09         | Summarization Failure Handling    | Simulate LLM failure and check error handling                 | 1. Mock a failure in `OpenAIClient.summarize()`. 2. Call `Summarizer.summarize_pdf()`.                                                              | Proper error should be displayed in the UI.    |
| TC_10         | Performance - PDF Processing Time | Ensure PDF processing time is reasonable                      | 1. Start timer. 2. Extract text and summarize. 3. Assert that total time is below a threshold (e.g., 10 seconds).                                    | Processing should complete within 10 seconds.  |

---

### **7. Entry and Exit Criteria**

#### **Entry Criteria:**
- All required components (PDF extraction, summarization, UI) have been implemented.
- The test environment has been set up, and dependencies installed.

#### **Exit Criteria:**
- All critical test cases have passed.
- No major defects remain unresolved.
- System is stable for user interaction and delivers summaries as expected.

---

### **8. Deliverables**

- Test scripts written in `pytest`.
- Test reports with pass/fail status for each test case.
- Performance report indicating the time taken to process PDFs.
- Issue/bug reports for any failures encountered.

---

### **9. Risks and Assumptions**

#### **Risks:**
- A slow or unavailable local Ollama server could lead to summarization failures or timeouts.
- Compatibility issues on different operating systems.
- Streamlit UI compatibility issues in different browsers.
- Summary quality varies significantly with the chosen Ollama model size.

#### **Assumptions:**
- Ollama is installed, running, and has the configured model (`OLLAMA_MODEL`) pulled during the test period.
- No internet connectivity is required for summarization itself, since inference runs locally.
- PDF files used for testing are valid and can be processed.

---

### **10. Schedule**

- **Test Case Development**: 2 days
- **Test Execution**: 3 days
- **Bug Fixing & Retesting**: 2 days
- **Test Closure**: 1 day

---

### **11. Tools**

- **Test Framework**: pytest
- **Linting**: ruff
- **CI/CD Tool**: GitHub Actions (`.github/workflows/ci.yml` — lint + test on every push/PR)
- **IDE**: VSCode or PyCharm for test script development
- **Reporting**: pytest's built-in HTML reports

---

### **12. Conclusion**

This test plan ensures the core functionality of the PDF Summarizer project is thoroughly tested for performance, reliability, and usability. By using a structured approach, the project will be ready for deployment with minimal risk of critical failures.

--- 

This **Test Plan** provides clear guidance for all involved stakeholders, ensuring a smooth and thorough testing process.