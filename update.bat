git add ./  
git commit -m %date:~0,4%%date:~5,2%%date:~8,2%0%time:~1,1%%time:~3,2%%time:~6,2%
git branch -M Dev_issues
git push -u  -f  origin Dev_issues
pause