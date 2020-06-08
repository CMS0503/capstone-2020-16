import React, {useState} from 'react';
import PropTypes from 'prop-types';
import SwipeableViews from 'react-swipeable-views';
import { makeStyles, useTheme } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Tabs from '@material-ui/core/Tabs';
import Tab from '@material-ui/core/Tab';
import Typography from '@material-ui/core/Typography';
import Box from '@material-ui/core/Box';
import Checkbox1 from './Checkbox1-1';
import Checkbox2 from './Checkbox1-2';
import Checkbox3 from './Checkbox2-1';
import Checkbox4 from './Checkbox2-2';
import Checkbox5 from './Checkbox3-1';
import Checkbox6 from './Checkbox3-2';
import Checkbox7 from './Checkbox4-1';
import Checkbox8 from './Checkbox4-2';








function TabPanel(props) {
  const { children, value, index, ...other } = props;


  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`full-width-tabpanel-${index}`}
      aria-labelledby={`full-width-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box p={2}>
          <Typography>{children}</Typography>
        </Box>
      )}
    </div>
  );
}

TabPanel.propTypes = {
  children: PropTypes.node,
  index: PropTypes.any.isRequired,
  value: PropTypes.any.isRequired,
};

function a11yProps(index) {
  return {
    id: `full-width-tab-${index}`,
    'aria-controls': `full-width-tabpanel-${index}`,
  };
}



const useStyles = makeStyles((theme) => ({
  root: {
    backgroundColor: theme.palette.background.paper,
    width: 900,
  },

  root: {
    backgroundColor: theme.palette.background.paper,
    width: 1250,
    position: 'center',
    minHeight: 450,
  },
}));




export default function FullWidthTabs() {
  const classes = useStyles();
  const theme = useTheme();
  const [value, setValue] = React.useState(0);
  

  const handleChange = (event, newValue) => {
    setValue(newValue);

  };


  const handleChangeIndex = (index) => {
    setValue(index);
  };
  

  return (
    
    <div className={classes.root}>
      <div>

      </div>	
      <AppBar position="static" color="default">
        <Tabs
          value={value}
          onChange={handleChange}
          indicatorColor="primary"
          textColor="primary"
          variant="fullWidth"
          aria-label="full width tabs example"
        >
          <Tab label="첫번 째 돌 선택" {...a11yProps(0)} />
          <Tab label="두번 째 돌 선택" {...a11yProps(1)} />
          <Tab label="세번 째 돌 선택" {...a11yProps(2)} />
          <Tab label="네번 째 돌 선택" {...a11yProps(3)} />

        </Tabs>
      </AppBar>
      <SwipeableViews
        axis={theme.direction === 'rtl' ? 'x-reverse' : 'x'}
        index={value}
        onChangeIndex={handleChangeIndex}
      >
        <TabPanel value={value} index={0} dir={theme.direction}>
          <div>
        <Checkbox1/><Checkbox2/>
          </div>
        </TabPanel>
        <TabPanel value={value} index={1} dir={theme.direction}>
          <div>
        <Checkbox3/><Checkbox4/>
          </div>
        </TabPanel>
        <TabPanel value={value} index={2} dir={theme.direction}>
          <div>
        <Checkbox5/><Checkbox6/>
          </div>
        </TabPanel>
        <TabPanel value={value} index={3} dir={theme.direction}>
          <div>
        <Checkbox7/><Checkbox8/>
          </div>
        </TabPanel>
      </SwipeableViews>
    </div>
  );
}




