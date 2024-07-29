import React from 'react';
import { Container, Typography, Paper, Box, List, ListItem, ListItemText } from '@mui/material';

const WelcomeCenter = () => {
  return (
    <Container maxWidth="md">
      <Box mt={4}>
        <Typography variant="h4" gutterBottom>
          Welcome to the Call Analyzer & Web Scraper Documentation
        </Typography>

        <Paper elevation={3} style={{ padding: '20px', marginTop: '20px' }}>
          <Typography variant="h5" gutterBottom>
            Call Analyzer Documentation
          </Typography>
          <Typography variant="body1" gutterBottom>
            The Call Analyzer allows you to upload call recordings, which are then transcribed and analyzed for various criteria such as empathy, active listening, appointment scheduling, and HVAC/plumbing issues.
          </Typography>
          <Typography variant="h6" gutterBottom>
            Steps to Use:
          </Typography>
          <List>
            <ListItem>
              <ListItemText primary="1. Upload the call recording by providing the file URL." />
            </ListItem>
            <ListItem>
              <ListItemText primary="2. Click on the 'Analyze Call' button." />
            </ListItem>
            <ListItem>
              <ListItemText primary="3. View the analysis results, which include a summary, detected issues, and agent feedback." />
            </ListItem>
          </List>
        </Paper>

        <Paper elevation={3} style={{ padding: '20px', marginTop: '20px' }}>
          <Typography variant="h5" gutterBottom>
            Web Scraper Documentation
          </Typography>
          <Typography variant="body1" gutterBottom>
            The Web Scraper allows you to extract data from web pages for further analysis. You can use it to scrape text, images, links, and other elements from specified URLs.
          </Typography>
          <Typography variant="h6" gutterBottom>
            Steps to Use:
          </Typography>
          <List>
            <ListItem>
              <ListItemText primary="1. Enter the URL of the web page you want to scrape." />
            </ListItem>
            <ListItem>
              <ListItemText primary="2. Select the elements you want to scrape (e.g., text, images)." />
            </ListItem>
            <ListItem>
              <ListItemText primary="3. Click on the 'Scrape' button." />
            </ListItem>
            <ListItem>
              <ListItemText primary="4. View the scraped data in the results section." />
            </ListItem>
          </List>
        </Paper>

        <Paper elevation={3} style={{ padding: '20px', marginTop: '20px' }}>
          <Typography variant="h5" gutterBottom>
            API Endpoints
          </Typography>
          <Typography variant="body1" gutterBottom>
            The following API endpoints are available for integration with the Call Analyzer and Web Scraper:
          </Typography>
          <Typography variant="h6" gutterBottom>
            Call Analyzer API:
          </Typography>
          <List>
            <ListItem>
              <ListItemText primary="POST /analyze-call - Analyzes a call recording." />
            </ListItem>
          </List>
          <Typography variant="h6" gutterBottom>
            Web Scraper API:
          </Typography>
          <List>
            <ListItem>
              <ListItemText primary="POST /scrape - Scrapes data from the specified URL." />
            </ListItem>
          </List>
        </Paper>
      </Box>
    </Container>
  );
};

export default WelcomeCenter;