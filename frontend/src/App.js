import React, { useEffect, useState } from 'react';
import './App.css';
import io from 'socket.io-client';
import Grid from '@material-ui/core/Grid/Grid';
import Box from '@material-ui/core/Box';
import Card from '@material-ui/core/Card';
import { Typography } from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';
import dayjs from 'dayjs';

const useStyles = makeStyles({
  root: {
    padding: '60px',
    backgroundColor: '#FAFAFA',
  },
  topBox: {
    height: '300px',
    width: '300px',
    color: '#4159E1',
    borderRadius: '15px',
    backgroundColor: 'white',
  },
  bottomBox: {
    height: '300px',
    width: '300px',
    borderRadius: '15px',
    color: 'white',
    backgroundColor: '#4159E1',
  },
  descriptionBox: {
    backgroundColor: 'white',
    borderRadius: '15px',
  },
  chart: {
    height: '64vh',
    backgroundColor: 'white',
    borderRadius: '15px',
  },
});

const server = 'http://localhost:5000';
const socket = io.connect(server);

const App = () => {
  const [count, setCount] = useState(0);
  useEffect(() => {
    socket.on('newNumber', (res) => {
      console.log(res.number);
      setCount(count + res.number);
    });
  }, [count]);
  const classes = useStyles();
  const date = dayjs().format('dddd, MMMM D, YYYY h:mm A');
  return (
    <div className={classes.root}>
      <Grid container spacing={2}>
        <Grid item xs={12}>
          <Typography variant="h3">Customer counting thingo</Typography>
          <Typography variant="subtitle2">{date}</Typography>
        </Grid>
        <Grid item xs={12}>
          <Grid container spacing={4}>
            <Grid item xs={7}>
              <Grid container spacing={2} alignItems="stretch">
                <Grid item xs={12}>
                  <Grid container className={classes.descriptionBox}>
                    <Grid item>
                      <Box p={4}>
                        <Typography>
                          This website tracks the number of customers in a store
                        </Typography>
                      </Box>
                    </Grid>
                  </Grid>
                </Grid>
                <Grid item xs={12}>
                  <Grid container className={classes.chart}>
                    <Grid item>
                      <Box p={4} style={{ height: '100%' }}>
                        <Typography>
                          This is where the chart will be{' '}
                        </Typography>
                      </Box>
                    </Grid>
                  </Grid>
                </Grid>
              </Grid>
            </Grid>
            <Grid item xs={5}>
              <Grid container spacing={2}>
                <Grid item xs={12}>
                  <Grid
                    container
                    className={classes.topBox}
                    alignItems="center"
                  >
                    <Grid item xs={12}>
                      <Typography variant="h1" align="center">
                        {count}
                      </Typography>
                      <Typography variant="subtitle1" align="center">
                        Current customers
                      </Typography>
                    </Grid>
                  </Grid>
                </Grid>
                <Grid item xs={12}>
                  <Grid
                    container
                    className={classes.bottomBox}
                    alignItems="center"
                  >
                    <Grid item xs={12}>
                      <Typography variant="h1" align="center">
                        30
                      </Typography>
                      <Typography variant="subtitle1" align="center">
                        Maximum capacity
                      </Typography>
                    </Grid>
                  </Grid>
                </Grid>
              </Grid>
            </Grid>
          </Grid>
        </Grid>
      </Grid>
    </div>
  );
};
export default App;
