# Tutorial on activating Jupyter Notebook in AWS Ubuntu Instance
_Jupyter is automatically installed via the bash script `setup.sh`._

1. Activate your Ubuntu instance as per normal in your local terminal/Powershell instance.
2. Run `setup.sh` if you have not already.
3. Run the following commands:
   ```
   export PATH=$PATH:~/.local/bin
   jupyter notebook --no-browser --port=8888
   ```
   This activates the Jupyter server on your remote instance, and provide you with a link to use to connect to the Jupyter server.
4. Open a second terminal/Powershell instance. Run the following command with your `.pem` file:
5. ```
   ssh -i <your-pem-file.pem> -L 8888:localhost:8888 ubuntu@<ssh-ip-address>
   ```
6. Access the Jupyter server using the provided links from step 3. 
