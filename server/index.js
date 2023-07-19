import express from 'express';
import { exec } from 'child_process';

import { fileURLToPath } from 'url';
import path,{join} from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Create Express server
const app = express();
const port = 3000;
const client=join(__dirname,"../client")
// Middleware to parse JSON request body
app.use(express.json());

// Define routes
app.post('/', (req, res) => {
  // Get input from req.body
  const input = req.body.input;
  console.log(input)

  // Run the Python script with input from req.body
  const pythonProcess = exec('instagram.py', (error, stdout, stderr) => {
    if (error) {
      console.error(`Error executing Python script: ${error}`);
      res.status(500).send('Error executing Python script');
      return;
    }
    console.log(`Python script output: ${stdout}`);
    res.send('Python script executed successfully');
  });

  // Pass input from req.body to the Python script through stdin
  pythonProcess.stdin.write(input);
  pythonProcess.stdin.end();

  // Handle the script's stdout and stderr
  pythonProcess.stdout.on('data', (data) => {
    console.log(`Python script stdout: ${data}`);
  });

  pythonProcess.stderr.on('data', (data) => {
    console.error(`Python script stderr: ${data}`);
  });
});

app.use(express.static(client));


// Start the server
app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
