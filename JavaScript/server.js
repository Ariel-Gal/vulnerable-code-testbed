const express = require('express');
const { exec } = require('child_process');
const app = express();

app.get('/ping', (req, res) => {
    const target = req.query.target || 'localhost';
    exec('ping -c 4 ' + target, (error, stdout, stderr) => {
        if (error) {
            res.send(error.message);
            return;
        }
        res.send(stdout);
    });
});

app.listen(3000);