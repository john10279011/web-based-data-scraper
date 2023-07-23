import express from 'express';
import { exec } from 'child_process';
import fs from 'fs';
import { fileURLToPath } from 'url';
import path, { join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Create Express server
const app = express();
const port = 3000;
const client = join(__dirname, '../client');

// Middleware to parse JSON request body
app.use(express.json());

// Define routes
app.post('/', (req, res, next) => {
  // Get input from req.body
  const input = req.body.input;
  console.log(input);

  // Run the Python script with input from req.body
  const pythonProcess = exec('instagram.py', (error, stdout, stderr) => {
    if (error) {
      console.error(`Error executing Python script: ${error}`);
      res.status(500).send('Error executing Python script');
      return;
    }
    console.log(`Python script output: ${stdout}`);

  
    scriptFinished();
  });


  pythonProcess.stdin.write(input);
  pythonProcess.stdin.end();

  pythonProcess.stdout.on('data', (data) => {
    console.log(`Python script stdout: ${data}`);
  });

  pythonProcess.stderr.on('data', (data) => {
    console.error(`Python script stderr: ${data}`);
  });


  function scriptFinished() {
fs.access('data.csv', fs.constants.F_OK, (accessError) => {
      if (accessError) {
        console.error(`data.csv file not found: ${accessError}`);
        res.status(500).send('Error generating data.csv');
      } else {
       // Send the data.csv file as a downloadable response
      const filePath = path.join(__dirname, 'data.csv');
      res.setHeader('Content-disposition', 'attachment; filename=data.csv');
      res.setHeader('Content-type', 'text/csv');

      res.download(filePath, 'data.csv', (downloadError) => {
        if (downloadError) {
          console.error(`Error downloading data.csv file: ${downloadError}`);
        } else {
          // File download successful, now delete the file from the server
          fs.unlink(filePath, (deleteError) => {
            if (deleteError) {
              console.error(`Error deleting data.csv file: ${deleteError}`);
            } else {
              console.log('data.csv deleted successfully');
            }
          })}});
          
       
      }
    });

  }
});




app.use(express.static(client));

// Start the server
app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
