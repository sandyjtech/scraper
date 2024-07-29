import React, { useState } from "react";
import axios from "axios";
import {
  Container,
  TextField,
  Button,
  Typography,
  CircularProgress,
  Box,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableRow,
  Paper,
} from "@mui/material";
import fileDownload from "js-file-download";
import htmlDocx from "html-docx-js/dist/html-docx";

const CallAnalyzer = () => {
  const [fileUrl, setFileUrl] = useState("");
  const [analysisResult, setAnalysisResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const response = await axios.post("/analyze-call", { file_url: fileUrl });
      setAnalysisResult(response.data);
    } catch (err) {
      setError("An error occurred while analyzing the call.");
    } finally {
      setLoading(false);
    }
  };
  const yesNo = (value) => (value === true ? "Yes" : "No");
  const generateDocContent = () => {
    if (!analysisResult) return "";

    return `
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Call Analysis Report - Balanced Comfort</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 0;
                    background-color: #f4f4f4;
                    color: #333;
                }
                .container {
                    width: 80%;
                    margin: 20px auto;
                    padding: 20px;
                    background-color: #fff;
                    border-radius: 8px;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                }
                h2 {
                    color: #19305a;
                    text-align: center;
                    margin-bottom: 20px;
                }
                table {
                    width: 100%;
                    border-collapse: collapse;
                    margin-bottom: 20px;
                }
                th, td {
                    padding: 10px;
                    text-align: left;
                    border-bottom: 1px solid #ddd;
                }
                th {
                    background-color: #19305a;
                    color: #fff;
                }
                tr:nth-child(even) {
                    background-color: #f9f9f9;
                }
                tr:hover {
                    background-color: #f1f1f1;
                }
                .section-title {
                    font-size: 1.4em;
                    margin-top: 20px;
                    margin-bottom: 10px;
                    color: #81c343;
                }
                .call-summary, .agent-feedback, .call-transcript {
                    padding: 15px;
                    background-color: #e8f8f5;
                    border-left: 5px solid #81c343;
                    border-radius: 5px;
                    margin-bottom: 20px;
                    white-space: pre-wrap;
                }
                .agent-feedback {
                    background-color: #e0f4e9;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h2>Call Analysis Report - Balanced Comfort</h2>
                <table>
                    <tr>
                        <th>Date</th>
                        <td>${analysisResult.date || "N/A"}</td>
                    </tr>
                    <tr>
                        <th>Agent</th>
                        <td>${analysisResult.agent || "N/A"}</td>
                    </tr>
                    <tr>
                        <th>Customer</th>
                        <td>${analysisResult.customer || "N/A"}</td>
                    </tr>
                    <tr>
                        <th>Inbound Number</th>
                        <td>${analysisResult.inbound_number || "N/A"}</td>
                    </tr>
                    <tr>
                        <th>Department</th>
                        <td>${analysisResult.department || "N/A"}</td>
                    </tr>
                    <tr>
                        <th>Service Category</th>
                        <td>${analysisResult.service_category || "N/A"}</td>
                    </tr>
                    <tr>
                        <th>Earliest Appointment</th>
                        <td>${analysisResult.earliest_appointment || "N/A"}</td>
                    </tr>
                    <tr>
                        <th>Lead Source</th>
                        <td>${analysisResult.lead_source || "N/A"}</td>
                    </tr>
                    <tr>
                        <th>Existing Customer?</th>
                        <td>${yesNo(analysisResult.existing_customer)}</td>
                    </tr>
                    <tr>
                        <th>Cloze Id</th>
                        <td>${analysisResult.cloze_id || "N/A"}</td>
                    </tr>
                    <tr>
                        <th>Sera Id</th>
                        <td>${analysisResult.sera_id || "N/A"}</td>
                    </tr>
                    <tr>
                        <th>Connex Id</th>
                        <td>${analysisResult.connex_id || "N/A"}</td>
                    </tr>
                </table>

                <div class="section-title">Call Summary</div>
                <div class="call-summary">
                    ${analysisResult.brief_summary || "N/A"}
                </div>
                <div class="section-title">Agent Feedback</div>
                <div class="agent-feedback">
                   ${analysisResult.notes || "N/A"}
                </div>
                <div class="section-title">Agent Opportunities:</div>
                <table>
                    <tr>
                        <th>Opening & Intro</th>
                        <td>${yesNo(analysisResult.good_opening)}</td>
                    </tr>
                    <tr>
                        <th>Branding</th>
                        <td>${analysisResult.brand_mentions || 0}</td>
                    </tr>
                    <tr>
                        <th>Active Listening</th>
                        <td>${yesNo(analysisResult.active_listening)}</td>
                    </tr>
                    <tr>
                        <th>Empathy</th>
                        <td>${yesNo(analysisResult.empathy)}</td>
                    </tr>
                    <tr>
                        <th>Clarity</th>
                        <td>${yesNo(analysisResult.clarity)}</td>
                    </tr>
                    <tr>
                        <th>Potential Services</th>
                        <td>${analysisResult.potential_services || "N/A"}</td>
                    </tr>
                    <tr>
                        <th>Warranties mentioned?</th>
                        <td>${yesNo(analysisResult.warranties_told)}</td>
                    </tr>
                    <tr>
                        <th>Problem Solver</th>
                        <td>${yesNo(analysisResult.problem_solving_skills)}</td>
                    </tr>
                    <tr>
                        <th>Upsell</th>
                        <td>${yesNo(analysisResult.upsell_opportunity)}</td>
                    </tr>
                    <tr>
                        <th>Closing (Recap)</th>
                        <td>${yesNo(analysisResult.closing_recap)}</td>
                    </tr>
                    <tr>
                        <th>Sentiment</th>
                        <td>${analysisResult.sentiment || "N/A"}</td>
                    </tr>
                    <tr>
                        <th>Complaint?</th>
                        <td>${yesNo(
                          analysisResult.complaint_about_employee
                        )}</td>
                    </tr>
                </table>
                
                <div class="section-title">Call Transcript</div>
                <div class="call-transcript">
                    ${analysisResult.transcript || "N/A"}
                </div>
            </div>
        </body>
        </html>`;
  };

  const handleDownload = () => {
    const docContent = generateDocContent();
    const docBlob = htmlDocx.asBlob(docContent);
    fileDownload(docBlob, "Call_Analysis_Report.docx");
  };

  return (
    <Container>
      <Typography variant="h4" align="center" gutterBottom>
        Call Analysis Report - Balanced Comfort
      </Typography>
      <form onSubmit={handleSubmit}>
        <Box mb={2}>
          <TextField
            fullWidth
            label="File URL"
            variant="outlined"
            value={fileUrl}
            onChange={(e) => setFileUrl(e.target.value)}
            required
          />
        </Box>
        <Box mb={2} textAlign="center">
          <Button
            type="submit"
            variant="contained"
            color="primary"
            disabled={loading}
          >
            Analyze
          </Button>
        </Box>
      </form>

      {loading && (
        <Box textAlign="center">
          <CircularProgress />
        </Box>
      )}
      {error && (
        <Typography color="error" align="center">
          {error}
        </Typography>
      )}
      {analysisResult && (
        <div>
          <TableContainer component={Paper}>
            <Table>
              <TableBody>
                <TableRow>
                  <TableCell>Date</TableCell>
                  <TableCell>{analysisResult.date || "N/A"}</TableCell>
                </TableRow>
                <TableRow>
                  <TableCell>Agent</TableCell>
                  <TableCell>{analysisResult.agent || "N/A"}</TableCell>
                </TableRow>
                <TableRow>
                  <TableCell>Customer</TableCell>
                  <TableCell>{analysisResult.customer || "N/A"}</TableCell>
                </TableRow>
                <TableRow>
                  <TableCell>Inbound Number</TableCell>
                  <TableCell>
                    {analysisResult.inbound_number || "N/A"}
                  </TableCell>
                </TableRow>
                <TableRow>
                  <TableCell>Department</TableCell>
                  <TableCell>{analysisResult.department || "N/A"}</TableCell>
                </TableRow>
                <TableRow>
                  <TableCell>Service Category</TableCell>
                  <TableCell>
                    {analysisResult.service_category || "N/A"}
                  </TableCell>
                </TableRow>
                <TableRow>
                  <TableCell>Earliest Appointment</TableCell>
                  <TableCell>
                    {analysisResult.earliest_appointment || "N/A"}
                  </TableCell>
                </TableRow>
                <TableRow>
                  <TableCell>Lead Source</TableCell>
                  <TableCell>{analysisResult.lead_source || "N/A"}</TableCell>
                </TableRow>
                <TableRow>
                  <TableCell>Existing Customer?</TableCell>
                  <TableCell>
                    {yesNo(analysisResult.existing_customer)}
                  </TableCell>
                </TableRow>
                <TableRow>
                  <TableCell>Cloze Id</TableCell>
                  <TableCell>{analysisResult.cloze_id || "N/A"}</TableCell>
                </TableRow>
                <TableRow>
                  <TableCell>Sera Id</TableCell>
                  <TableCell>{analysisResult.sera_id || "N/A"}</TableCell>
                </TableRow>
                <TableRow>
                  <TableCell>Connex Id</TableCell>
                  <TableCell>{analysisResult.connex_id || "N/A"}</TableCell>
                </TableRow>
              </TableBody>
            </Table>
          </TableContainer>

          <div className="section-title">Call Summary</div>
          <div className="call-summary">
            {analysisResult.brief_summary || "N/A"}
          </div>

          <div className="section-title">Agent Feedback</div>
          <div className="agent-feedback">{analysisResult.notes || "N/A"}</div>

          <div className="section-title">Agent Opportunities:</div>
          <TableContainer component={Paper}>
            <Table>
              <TableBody>
                <TableRow>
                  <TableCell>Opening & Intro</TableCell>
                  <TableCell>{yesNo(analysisResult.good_opening)}</TableCell>
                </TableRow>
                <TableRow>
                  <TableCell>Branding</TableCell>
                  <TableCell>{analysisResult.brand_mentions || 0}</TableCell>
                </TableRow>
                <TableRow>
                  <TableCell>Active Listening</TableCell>
                  <TableCell>
                    {yesNo(analysisResult.active_listening)}
                  </TableCell>
                </TableRow>
                <TableRow>
                  <TableCell>Empathy</TableCell>
                  <TableCell>{yesNo(analysisResult.empathy)}</TableCell>
                </TableRow>
                <TableRow>
                  <TableCell>Clarity</TableCell>
                  <TableCell>{yesNo(analysisResult.clarity)}</TableCell>
                </TableRow>
                <TableRow>
                  <TableCell>Potential Services</TableCell>
                  <TableCell>
                    {analysisResult.potential_services || "N/A"}
                  </TableCell>
                </TableRow>
                <TableRow>
                  <TableCell>Warranties mentioned?</TableCell>
                  <TableCell>{yesNo(analysisResult.warranties_told)}</TableCell>
                </TableRow>
                <TableRow>
                  <TableCell>Problem Solver</TableCell>
                  <TableCell>
                    {yesNo(analysisResult.problem_solving_skills)}
                  </TableCell>
                </TableRow>
                <TableRow>
                  <TableCell>Upsell</TableCell>
                  <TableCell>
                    {yesNo(analysisResult.upsell_opportunity)}
                  </TableCell>
                </TableRow>
                <TableRow>
                  <TableCell>Closing (Recap)</TableCell>
                  <TableCell>{yesNo(analysisResult.closing_recap)}</TableCell>
                </TableRow>
                <TableRow>
                  <TableCell>Sentiment</TableCell>
                  <TableCell>{analysisResult.sentiment || "N/A"}</TableCell>
                </TableRow>
                <TableRow>
                  <TableCell>Complaint?</TableCell>
                  <TableCell>
                    {yesNo(analysisResult.complaint_about_employee)}
                  </TableCell>
                </TableRow>
              </TableBody>
            </Table>
          </TableContainer>

          <div className="section-title">Call Transcript</div>
          <div className="call-transcript">
            {analysisResult.transcript || "N/A"}
          </div>

          <Box mt={2} textAlign="center">
            <Button
              variant="contained"
              color="secondary"
              onClick={handleDownload}
            >
              Download Report as DOCX
            </Button>
          </Box>
        </div>
      )}
    </Container>
  );
};

export default CallAnalyzer;
