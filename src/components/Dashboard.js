// src/components/Dashboard.js
import React, { useState, useEffect } from 'react';
import { Container, Grid, CircularProgress, Snackbar, Alert } from '@mui/material';
import DishCard from './DishCard';
import axios from 'axios';
import '../index.css';

const Dashboard = () => {
  const [dishes, setDishes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchDishes = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8000/dishes');
        setDishes(response.data);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching dishes:', error);
        setError('Error fetching dishes');
        setLoading(false);
      }
    };

    fetchDishes();

    const eventSource = new EventSource('http://127.0.0.1:8000/events');
    eventSource.onmessage = function (event) {
      const data = JSON.parse(event.data);
      setDishes((prevDishes) =>
        prevDishes.map((dish) =>
          dish.dishId === data.dishId ? { ...dish, isPublished: data.isPublished } : dish
        )
      );
    };

    eventSource.onerror = function (event) {
      console.error('EventSource failed:', event);
      eventSource.close();
    };

    return () => {
      eventSource.close();
    };
  }, []);

  const handleToggle = (dishId) => {
    setDishes((prevDishes) =>
      prevDishes.map((dish) =>
        dish.dishId === dishId ? { ...dish, isPublished: !dish.isPublished } : dish
      )
    );
  };

  return (
    <Container>
      {loading ? (
        <div className="loading-spinner">
          <CircularProgress />
        </div>
      ) : (
        <Grid container spacing={3}>
          {dishes.map((dish) => (
            <Grid item xs={12} sm={6} md={4} lg={3} key={dish.dishId}>
              <DishCard dish={dish} onToggle={handleToggle} />
            </Grid>
          ))}
        </Grid>
      )}
      {error && (
        <Snackbar open={true} autoHideDuration={6000} onClose={() => setError(null)}>
          <Alert onClose={() => setError(null)} severity="error">
            {error}
          </Alert>
        </Snackbar>
      )}
    </Container>
  );
};

export default Dashboard;