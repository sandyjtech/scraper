import React, { useState } from "react";
import axios from "axios";
import { Container, TextField, Button, Typography, Box } from "@mui/material";


const ScraperForm = () => {
  const [formData, setFormData] = useState({
    url: "",
    username: "",
    password: "",
    class_name: "",
    button_class: "",
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post(
        "http://localhost:5000/scraper",
        formData
      );
      console.log(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <Container maxWidth="sm">
      <Box
        component="form"
        onSubmit={handleSubmit}
        sx={{
          display: "flex",
          flexDirection: "column",
          gap: 2,
          mt: 5,
          p: 3,
          backgroundColor: "background.paper",
          borderRadius: 2,
          boxShadow: 1,
        }}
      >
        <Typography variant="h4" color="primary" align="center">
          Web Scraper
        </Typography>
        <TextField
          label="URL"
          name="url"
          value={formData.url}
          onChange={handleChange}
          required
          fullWidth
        />
        <TextField
          label="Username"
          name="username"
          value={formData.username}
          onChange={handleChange}
          required
          fullWidth
        />
        <TextField
          label="Password"
          name="password"
          type="password"
          value={formData.password}
          onChange={handleChange}
          required
          fullWidth
        />
        <TextField
          label="Class Name"
          name="class_name"
          value={formData.class_name}
          onChange={handleChange}
          required
          fullWidth
        />
        <TextField
          label="Button Class"
          name="button_class"
          value={formData.button_class}
          onChange={handleChange}
          fullWidth
        />
        <Button type="submit" variant="contained" color="primary">
          Scrape
        </Button>
      </Box>
    </Container>
  );
};

export default ScraperForm;
