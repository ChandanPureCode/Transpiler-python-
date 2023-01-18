import {Card, Stack, CardMedia, Stack, CardContent, Stack, Typography, Typography, Stack, CardActions, IconButton, Icon} from '@mui/material';import AuthorDetails from './AuthorDetails';function BlogCard(){ return (<Card sx = { {width:"900px",height:"360px",display:"grid",placeItems:"center",borderRadius:"20px",}}><Stack margin= {1} spacing= {2} direction = "row" sx = { {alignItems:"center",width:"calc(100% - 1rem)",height:"calc(100% - 1rem)",}}><CardMedia component = "img" src = "https://images.unsplash.com/photo-1505807557511-bc38492556a6" alt = "leaves" sx = { {height:"340px",borderRadius:"16px",aspectRatio:"4/3",}}/><Stack sx = { {height:"100%",justifyContent:"space-around",}}><CardContent><Stack spacing= {2}><Typography fontWeight= {600} fontSize = "1.3rem">Green plants are going to extinct about 500 times faster than they should, study finds</Typography><Typography>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean sit amet efficitur sem, id blandit justo.</Typography></Stack></CardContent><Stack direction = "row" sx = { {justifyContent:"space-between",}}><AuthorDetails authorImageSource = "https://images.unsplash.com/photo-1494790108377-be9c29b29330" authorName = "Remy Sharp" dateOfPublication = "July 22, 2022"/><CardActions><IconButton aria-label = "share"><Icon>share</Icon></IconButton></CardActions></Stack></Stack></Stack></Card>)}