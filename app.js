#!/usr/bin/env python
const express = require("express");
const app = express();
const fs=require('fs');
const csv = require('csv-parse');
const bodyParser = require("body-parser");
const upload=require("express-fileupload");
var nodemailer = require('nodemailer');
var mv=require('mv');
var spawn = require('child_process').spawn
var child = spawn('pwd')
var alert=require('alert')
const results = [];
const port=process.env.PORT || 3000;
app.use(upload());
app.use(express.static("public"));
app.use(bodyParser.urlencoded({
  extended: true
}));
app.get("/", function(req, res) {
  res.sendFile(__dirname+"/index.html");
});
app.post("/", function(request, response) {
  // Reading Python files
  var fileName;
  if(request.files){
    var file=request.files.file;
    fileName=file.name;
    file.mv(__dirname+"/"+fileName,function(err){
      if(err){
        response.send(err);
      }
    });
  }
  //spawn new child process to call the python script
  const python = spawn('python', [__dirname+'/102003070.py', __dirname+'/'+fileName, request.body.weight, request.body.impact, __dirname+'/output.csv']);
  // collect data from script
  var dataToSend,flag=0;
  python.stdout.on('data', function(data) {
    dataToSend = data.toString();
    flag=1;
  });
  python.stderr.on('data', data => {
    console.error('stderr: ${data}');
  }); // in close event we are sure that stream from child process is closed
  python.on('exit', (code) =>{
    if(flag==1){
      response.send(dataToSend);
    }

    let transporter = nodemailer.createTransport({
      host: 'smtp.gmail.com',
      port:465,
      sender:'gmail',
      auth: {
          user: 'gsingh102003@gmail.com', // my mail
          pass: 'erbaazraounsrsqp'
        }
      });
      if(flag==0){

    var mailOptions = {
      from: 'gsingh102003@gmail.com',
      to: request.body.email,
      subject: 'Result of topsis',
      text:'Result of Input file : ',
      attachments: [{ // utf-8 string as an attachment
        filename:'output.csv',path: __dirname+'/output.csv'
      }]
    };
}
if(flag==1){
  var mailOptions = {
    from: 'gsingh102003@gmail.com',
    to: request.body.email,
    subject: 'Result of topsis',
    text: dataToSend
  };
}
    try {
  fs.unlinkSync(__dirname+'/'+fileName);
  console.log("Delete File successfully.");
  } catch (error) {
  console.log(error);
  }
    transporter.sendMail(mailOptions, function(error, info) {
      if (error) {
        console.log(error);
      } else {
        console.log('Email sent ');
      }
    });
    if(flag==0){
      response.sendFile(__dirname+"/success.html");
    }
  });
});
app.listen(port, function() {
  console.log("server started");
})
