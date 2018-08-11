# JORY.JY
Selenium powered Python script to automate searching the web for vulnerable applications.

DorkNet can take a single dork or a list of dorks as arguments. After the proper command line arguments have been passed, the script will use Selenium and Geckodriver to find the results we want and save them to a textfile for further processing with SQLmap or similar utilities.

## Usage

```
git clone git@github.com:joryvps/web.git
cd DorkNet
python dorknet.py
```

The options for the program are as follows.

```
-h, --help              show this help message and exit
-d DORK, --dork DORK    specify the dork you wish to use
-l LIST, --list LIST    specify path to list with dorks
-v, --verbose           toggle verbosity
```

Some examples for clarity.

```
DorkNet.py -h
DorkNet.py -d inurl:show.php?id= -v
DorkNet.py -l /path/to/list.txt --verbose
```

**Proxifying**

I have included the ability to proxy the connection of the web driver if desired. Simply provide the proxy IP and PORT when the dialog comes up and the search engine will be accessed via the proxy settings you have provided. 


### Dependencies

You will need the Mozilla [Geckodriver](https://github.com/mozilla/geckodriver/releases) for this to work. You can install it manually. However i've added a shell script to automate the process if you'd prefer.

To use it, navigate to the DorkNet directory and make the shell script executable like so.

```
cd DorkNet
chmod +x gecko-setup.sh

# Execute the shell script with the below command.
sudo ./gecko-setup.sh
```
The shell script has an option to automatically install the rest of the dependencies as well, via the requirements file, by invoking the following commands.

```sudo -H pip install -r requirements.txt```

### Note

DorkNet is featured in the [BlackArch Linux](https://blackarch.org) PenTesting Distro under WebApp Tools & Automation. As such it comes pre-installed with the distro. Reference the relevant [PKGBUILD](https://github.com/BlackArch/blackarch/blob/master/packages/dorknet/PKGBUILD) file in it's respective repo for details.


### Known Issue
By using Selenium and Geckodriver, DorkNet is effective at emulating a regular browser. In this manner the program is able to avoid captchas most of the time. However on limited occasions, Google throws one regardless. The same sometimes happens when manually searching for strings that look like a dork. Should you encounter one, you can just fill out the captcha in the Geckodriver and DorkNet will continue it's normal operation.
