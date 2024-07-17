// src/components/DishCard.js
import React from 'react';
import { Card, CardMedia, CardContent, Typography, Button } from '@mui/material';
import { motion } from 'framer-motion';
import axios from 'axios';
import '../index.css';

const DishCard = ({ dish, onToggle }) => {
  const handleToggle = async () => {
    try {
      await axios.post(`http://127.0.0.1:8000/dishes/toggle/${dish.dishId}`);
      onToggle(dish.dishId);
    } catch (error) {
      console.error('Error toggling dish status', error);
    }
  };

  return (
    <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
      <Card className="card">
        <CardMedia
          component="img"
          className="card-media"
          image={dish.imageUrl}
          alt={dish.dishName}
        />
        <CardContent className="card-content">
          <Typography gutterBottom variant="h5" component="div">
            {dish.dishName}
          </Typography>
          <Typography variant="body2" color="text.secondary">
            {dish.isPublished ? 'Published' : 'Unpublished'}
          </Typography>
          <Button
            variant="contained"
            color={dish.isPublished ? 'secondary' : 'primary'}
            onClick={handleToggle}
            className="button"
          >
            {dish.isPublished ? 'Unpublish' : 'Publish'}
          </Button>
        </CardContent>
      </Card>
    </motion.div>
  );
};

export default DishCard;