import React, { useState } from "react";
import { AppBar, Tabs, Tab, Container, Box, Typography } from "@mui/material";
import ScraperForm from "./components/ScraperForm";
import CallAnalyzer from "./components/CallAnalyzer";
import WelcomeCenter from "./components/WelcomeCenter";

function App() {
  const [activeTab, setActiveTab] = useState(0);

  const handleTabChange = (event, newValue) => {
    setActiveTab(newValue);
  };

  const renderActiveTab = () => {
    switch (activeTab) {
      case 0:
        return <WelcomeCenter />;
      case 1:
        return <ScraperForm />;
      case 2:
        return <CallAnalyzer />;
      default:
        return <WelcomeCenter />;
    }
  };

  return (
    <Container maxWidth="md">
      <Box mt={4}>
        <Typography variant="h4" align="center" gutterBottom>
          Call Analyzer & Web Scraper
        </Typography>
        <AppBar position="static" color="default">
          <Tabs
            value={activeTab}
            onChange={handleTabChange}
            indicatorColor="primary"
            textColor="primary"
            centered
          >
            <Tab label="Welcome Center" />
            <Tab label="Scraper Form" />
            <Tab label="Call Analyzer" />
          </Tabs>
        </AppBar>
        <Box mt={2}>
          {renderActiveTab()}
        </Box>
      </Box>
    </Container>
  );
}

export default App;
