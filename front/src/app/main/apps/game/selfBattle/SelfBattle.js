import FuseAnimate from '@fuse/core/FuseAnimate';
import FuseAnimateGroup from '@fuse/core/FuseAnimateGroup';
import Card from '@material-ui/core/Card';
import CardActions from '@material-ui/core/CardActions';
import Divider from '@material-ui/core/Divider';
import { makeStyles } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';
import clsx from 'clsx';
import React, { useEffect, useState } from 'react';
import { useDispatch } from 'react-redux';
import Button from "@material-ui/core/Button";
import * as Actions from 'app/store/actions';
import CardMedia from '@material-ui/core/CardMedia';
import axios from 'axios';
import CodeGrid from './components/CodeListGrid'

const useStyles = makeStyles(theme => ({
	header: {
		background: `linear-gradient(to right, ${theme.palette.primary.dark} 0%, ${theme.palette.primary.main} 100%)`,
		color: theme.palette.getContrastText(theme.palette.primary.main)
	},
	headerIcon: {
		position: 'absolute',
		top: -64,
		left: 0,
		opacity: 0.04,
		fontSize: 512,
		width: 512,
		height: 512,
		pointerEvents: 'none'
	}
}));


function Courses(props) {

	const dispatch = useDispatch();
	var header = {
		'Authorization' : 'jwt ' + window.localStorage.getItem('jwt_access_token')
	  }

	const classes = useStyles(props);

	const [posts, setPosts] = useState([]);
	
	const [battleId, setBattleId] = useState(-1);

	useEffect(() => {

		axios
		.get('http://203.246.112.32:8000/api/v1/problem/')
		.then(response => {
			dispatch(Actions.getProblemId(response.data.results));
			setPosts(response.data.results);
			window.sessionStorage.setItem('SS_ProblemId', response.data.results);
		})
	},[dispatch]);

	
	return (
		<div className="flex flex-col flex-auto flex-shrink-0 w-full">
			
			<div
				className={clsx(
					classes.header,
					'relative overflow-hidden flex flex-col flex-shrink-0 items-center justify-center text-center p-16 sm:p-24 h-200 sm:h-288'
				)}
			>
				<FuseAnimate animation="transition.slideUpIn" duration={400} delay={100}>
					<Typography color="inherit" className="text-24 sm:text-40 font-light">
					Me vs My Codes
					</Typography>
				</FuseAnimate>
				<FuseAnimate duration={400} delay={600}>
					<Typography variant="subtitle1" color="inherit" className="mt-8 sm:mt-16 mx-auto max-w-512">
						<span className="opacity-75">
						Welcome to Me vs My Codes. Choose a Game to Play!
						</span>
					</Typography>
				</FuseAnimate>
		
			</div>
			{battleId === -1 ?
			<div className="flex flex-col flex-1 max-w-2xl w-full mx-auto px-8 sm:px-16 py-24">
		
							<FuseAnimateGroup
								enter={{
									animation: 'transition.slideUpBigIn'
								}}
								className="flex flex-wrap py-24"
							>	
								{posts.map(problem => {
									return (
										<div className="w-full pb-24 sm:w-1/2 lg:w-1/3 sm:p-16" key={problem.title}>
											<Card elevation={1} className="flex flex-col h-256">
												<div
													className="flex flex-shrink-0 items-center justify-between px-24 h-64"
												>
													<Typography className="font-medium truncate" color="inherit">
														{problem.title}
													</Typography>
													
				
												</div>
												<CardMedia className="flex items-center justify-center">
												<img src={problem.thumbnail} 
													onClick = {() =>{
														window.sessionStorage.setItem('SS_SelectedProblemId', problem.id);
														setBattleId(problem.id);
													}}
													width='300' alt='thumbnail'></img>
												</CardMedia>
												

												<Divider />
												<CardActions className="justify-center" >
													 <button onClick = {() => {
														 window.sessionStorage.setItem('SS_SelectedProblemId', problem.id);
														 setBattleId(problem.id);
													 }}> Self Battle Start </button>
												<Divider orientation="vertical" flexItem />
												</CardActions>
												
											</Card>
										</div>
									);
								})}
							</FuseAnimateGroup>
						  
			</div>
			: <div style={{margin: 0, marginTop: 0, justifyContent: 'center'}}>
				<h1 style={{marginLeft: "15vw"}}>
					<Button variant="contained" color="secondary" onClick={()=>{setBattleId(-1);}}>
						Select other game
					</Button>
				</h1>
				<CodeGrid battleId={battleId}/>
				</div>}
		</div>
	);
}

// export default withReducer('academyApp', reducer)(Courses);

export default (Courses);
