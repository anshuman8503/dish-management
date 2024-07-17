// src/App.js
import React from 'react';
import { CssBaseline, Typography, AppBar, Toolbar } from '@mui/material';
import Dashboard from './components/Dashboard';
import './index.css';

function App() {
  return (
    <div className="App">
      <CssBaseline />
      <AppBar position="static" className="app-bar">
        <Toolbar>
          <Typography variant="h6" color="inherit" noWrap>
            Dish Information Management System
          </Typography>
        </Toolbar>
      </AppBar>
      <div className="container">
        <Dashboard />
      </div>
    </div>
  );
}

export default App;