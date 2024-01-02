FakeNewsDetector Project

The aim of the fake news project is to help news readers to identify bias and misinformation in news articles in a quick and reliable fashion.
              We have collected news articles with veracity labels from fact-checking websites and used them to train text classification systems to detect fake from real news. You can paste a piece of text and examine its similarity to our collection of true vs. false news articles, or to news from four different types/genre. Enjoy testing!


© 2024 Fake News Detector

How to Set up
1. First you have to install Docker at your Computer if you haven't already isntalled, following one by one these commands
   
  First, update your existing list of packages:
    sudo apt update
  Next, install a few prerequisite packages which let apt use packages over HTTPS:
    sudo apt install apt-transport-https ca-certificates curl software-properties-common
   
  Then add the GPG key for the official Docker repository to your system:
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    
  Add the Docker repository to APT sources:
    sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"
    
  Make sure you are about to install from the Docker repo instead of the default Ubuntu repo: 
    apt-cache policy docker-ce

  Finally, install Docker:
    sudo apt install docker-ce

  Docker should now be installed, the daemon started, and the process enabled to start on boot. Check that it’s running:
    sudo systemctl status docker

  Step 2 — Executing the Docker Command Without Sudo
  Avoid typing sudo whenever you run the docker command, add your username to the docker group:
    sudo usermod -aG docker ${USER}
  To apply the new group membership, log out of the server and back in, or type the following:
    su - ${USER}
    
2. Open the terminal in the folder where the project is and Run the command: sudo docker compose up -d
3. After installing the Images the project is almost done and working. One final step only need to change the access permissions for your WordPress Directory by using the followinf commands in the following path /Desktop/FakeNewsDetector/src :
    sudo chown -R www-data:www-data wp-content/plugins/
    sudo chmod 775 wp-content
    
    sudo chown -R www-data:www-data wp-content/
4. The wordpress index page is running on http://localhost:8000/

Thank for Installing and Enjoy Testing!
   
     
