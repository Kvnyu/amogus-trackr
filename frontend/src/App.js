import React, { useEffect, useState } from 'react';
import './App.css';
import io from 'socket.io-client';
import Grid from '@material-ui/core/Grid/Grid';
import Box from '@material-ui/core/Box';
import '@fontsource/karla';
import { Typography } from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';
import WarningIcon from '@material-ui/icons/Warning';

import dayjs from 'dayjs';
import {
  Sparkline,
  LineSeries,
  HorizontalReferenceLine,
  BandLine,
  PatternLines,
  PointSeries,
} from '@data-ui/sparkline';
import { allColors } from '@data-ui/theme';

const useStyles = makeStyles({
  root: {
    padding: '60px',
    backgroundColor: '#FAFAFA',
    fontFamily: 'Karla',
    marginLeft: 'auto',
    marginRight: 'auto',
    marginTop: '24px',
    marginBottom: '24px',
  },
  topBox: {
    height: '300px',
    width: '300px',
    color: (props) => (!props.overLimit ? '#3557E4' : '#FF4F4F'),
    borderRadius: '15px',
    backgroundColor: 'white',
  },
  bottomBox: {
    height: '300px',
    width: '300px',
    borderRadius: '15px',
    color: 'white',
    backgroundColor: '#3557E4',
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
  number: {
    fontWeight: '720px',
    fontSize: '104px',
  },
  numberDescription: {
    fontWeight: '600',
  },
  grey: {
    color: '#5F6582',
  },
});

const server = 'http://localhost:5000';
const socket = io.connect(server);
const App = () => {
  const limit = 30;
  const [count, setCount] = useState(0);
  // const [countData, setCountData] = useState([]);
  const [overLimit, setOverLimit] = useState(false);

  useEffect(() => {
    const handler = (res) => {
      setCount(count + res.number);
      // setCountData([...countData, count]);
      setOverLimit(count + res.number > limit);
      // console.log(countData);
    };
    socket.on('newNumber', handler);
    return () => socket.off('newNumber', handler);
  }, [count, overLimit]);

  const classes = useStyles({ overLimit });
  const date = dayjs().format('dddd, MMMM D, YYYY h:mm A');

  return (
    <div className={classes.root}>
      <Grid container spacing={2}>
        <Grid item xs={12}>
          <Typography variant="h3" style={{ color: '#13246C' }}>
            Customer Counter
          </Typography>
          <Typography variant="subtitle2" className={classes.grey}>
            {' '}
            {date}
          </Typography>
        </Grid>
        <Grid item xs={12}>
          <Grid container spacing={4}>
            <Grid item xs={9}>
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
                  <div style={{ padding: '32px', backgroundColor: 'white' }}>
                    <Grid container align row>
                      <Grid item xs={6}>
                        <Typography>Customer Tracker</Typography>
                      </Grid>
                      <Grid item xs={6}>
                        <Grid container justifyContent="flex-end">
                          <Grid item>
                            <div
                              style={{
                                backgroundColor: 'rgba(53, 87, 228, 0.17)',
                                borderRadius: '16px',
                                paddingTop: '4px',
                                paddingBottom: '4px',
                                paddingLeft: '8px',
                                paddingRight: '8px',
                              }}
                            >
                              <Typography style={{ color: '#3557E4' }}>
                                Today
                              </Typography>
                            </div>
                          </Grid>
                        </Grid>
                      </Grid>
                      <Grid
                        item
                        xs={12}
                        justifyContent="center"
                        alignItems="center"
                      >
                        {/*  */}
                      </Grid>
                    </Grid>
                  </div>
                </Grid>
              </Grid>
            </Grid>
            <Grid item xs={3}>
              <Grid container spacing={2}>
                <Grid item xs={12}>
                  <Grid
                    container
                    className={classes.topBox}
                    alignItems="center"
                  >
                    <div style={{ position: 'absolute' }}>
                      {overLimit && (
                        <div
                          style={{
                            position: 'absolute',
                            top: '-128px',
                            left: '16px',
                          }}
                        >
                          <WarningIcon styles={{ color: "'#FF4F4F'" }} />
                        </div>
                      )}
                    </div>

                    <Grid item xs={12}>
                      <Typography align="center" className={classes.number}>
                        {count}
                      </Typography>
                      <Typography
                        align="center"
                        className={classes.numberDescription}
                      >
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
                      <Typography align="center" className={classes.number}>
                        {limit}
                      </Typography>
                      <Typography
                        align="center"
                        className={classes.numberDescription}
                      >
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
