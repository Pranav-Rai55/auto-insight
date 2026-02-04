const express = require('express');
const app = express();
const bodyParser = require('body-parser');
const cors = require('cors');
const AuthRouter = require('./routes/authrouter.js');
const Connetdb = require("./database/db");
require('dotenv').config();

const PORT = process.env.PORT || 5000;
app.use(cors());            
app.use(express.json());

app.get('/', (req, res) => {
    res.send('PONG');
});
Connetdb();

app.use(bodyParser.json());
app.use(cors());
app.use('/auth', AuthRouter);


app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`)
})