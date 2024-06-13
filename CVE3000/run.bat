@echo off

echo Step 1: Installing Python 3.12.1...

REM Check Python version
python --version 2>&1 | findstr /R "Python [3-9]\.[1-9][2-9]\.[0-9]" > version.txt
if %ERRORLEVEL% EQU 0 (
    echo Python 3.12.1 or later is already installed.
) else (
    echo Python 3.12.1 not found or version is less than 3.12.1, downloading...
    REM Download and install Python 3.12.1 using wget
    curl -o python-3.12.1.exe https://www.python.org/ftp/python/3.12.1/python-3.12.1-amd64.exe
    start /wait python-3.12.1.exe InstallAllUsers=1 PrependPath=1
    del python-3.12.1.exe
    echo Please run this script again.
    pause
    exit /b
)

del version.txt
pause

echo Step 2: Checking for Node.js and npm...

REM Check if Node.js is installed
where node > nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Node.js not found, downloading...
    REM Download and install Node.js using curl
    curl -o nodejs.msi https://nodejs.org/dist/v16.17.0/node-v16.17.0-x64.msi
    msiexec /i nodejs.msi 
    del nodejs.msi
    echo Please run this script again.
    pause
    exit /b
) else (
    echo Node.js is already installed.
    REM Check Node.js version
    node --version 2>&1 | findstr /R "v16\.17\.0" > version.txt
    if %ERRORLEVEL% NEQ 0 (
        echo Incorrect Node.js version, updating...
        REM Download and install Node.js using curl
        curl -o nodejs.msi https://nodejs.org/dist/v16.17.0/node-v16.17.0-x64.msi
        msiexec /i nodejs.msi 
        del nodejs.msi
        echo Please run this script again.
    	pause
    	exit /b
    ) else (
        
        REM Check if npm is installed
        where npm > nul 2>&1
        if %ERRORLEVEL% NEQ 0 (
            echo npm not found, downloading...
            REM Download and install npm using curl
            curl -o nodejs.msi https://nodejs.org/dist/v16.17.0/node-v16.17.0-x64.msi
            msiexec /i npm.msi 
            del npm.msi
            echo Please run this script again.
	    pause
    	    exit /b
        ) else (
            echo npm is already installed.
            REM Check npm version
            npm --version 2>&1 | findstr /R "7\.13\.0" > version.txt
            if %ERRORLEVEL% NEQ 0 (
                echo Incorrect npm version, updating...
                REM Download and install npm using curl
                curl -o nodejs.msi https://nodejs.org/dist/v16.17.0/node-v16.17.0-x64.msi
                msiexec /i npm.msi 
                del npm.msi
                echo Please run this script again.
		        pause
    	    	exit /b
            ) 
        )
    )
)

del version.txt
echo Node.js and npm installed successfully.
pause

echo Step 3: Checking for Redis...

REM Check if Redis is installed
where redis-server > nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Redis not found, downloading...
    REM Download and install Redis using curl
    winget https://github.com/tporadowski/redis/releases/download/v5.0.14.1/Redis-x64-5.0.14.1.msi
    msiexec /i Redis-x64-5.0.14.1.msi 
    del Redis-x64-5.0.14.1.msi
    echo Please run this script again.
    pause
    exit /b
) else (
    echo Redis is already installed.
    REM Check Redis version
    redis-server -v > version.txt
    findstr /R "v=3\.0\.[0-9][0-9][0-9]" version.txt > nul 2>&1
    if %ERRORLEVEL% NEQ 0 (
        echo Incorrect Redis version, updating...
        REM Download and install Redis using curl
        winget https://github.com/tporadowski/redis/releases/download/v5.0.14.1/Redis-x64-5.0.14.1.msi
        msiexec /i Redis-x64-5.0.14.1.msi 
        del Redis-x64-5.0.14.1.msi
        echo Please run this script again.
        pause
        exit /b
    )
)

del version.txt
pause


echo Step 4: Creating server.bat...
REM Create server.bat
echo npm install express >> server.bat


echo Step 5: Running server.bat...
call server.bat 
REM Delete server.bat after execution
del server.bat

echo Step 6: Changing directory to see_me_first and starting Node.js server...
cd see_me_first
dir
start /B node server.js
cd ..

REM opens fill_me_first.html to let the user fill in
echo Step 7: Fill out fill_me_first.html
cd see_me_first
start http://localhost:3000/
cd ..
pause

