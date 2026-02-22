# Basics of Bash

## Builtin vs External Commands

**/bin/bash**: executable binary file of the BASH program itself
- **Builtin Commands**: commands that are inside the `/bin/bash` program and executed directly in the shell process
    - `help`: provides information for builtin commands
- **External Commands**: commands that are outside of the `/bin/{command}` and executed by a new forked process (specified by the `$PATH` environment variable)
    - `man`: provides information for external commands

`type`: builtin command that tells you where the command is located

`which`: external command that tells you if you are currently using a shell builtin command or the location of the external command being used

## Basic Commands

- **`ls`: list contents of working directory**
    - `-l`: long list format that shows permissions, users, modification time, etc. 
    - `-a`: includes hidden files (e.g. dotfiles)
    - `-h`: long list format with human readable file sizes
    - `-t`: sorts by time (most recent => least recent)
    - `-r`: reverse the sort (usually used with `-t`)
    - `-R`: recursively lists all the contents
    - `-S`: sort by size (largest => smallest)
    - `-1`: prints result of `ls` command with one per line (used when scripting)
    - `-d`: directories only 
    - `-F`: adds indication characters (e.g. `/` for directories, `*` for executables)
- `cd`: change directory 
    - `/`: root directory of the filesystem
    - `~`: user's home directory
    - `..`: up one directory level
    - `-`: previous working directory 
- `pwd`: print working directory
    - `-L`: print logical path (with symlinks)
    - `-P`: print physical path (without symlinks)
- `echo`: print text
    - `-n`: don't add newline character `\n` at the end 
    - `-e`: enable backslash escape characters 
    - `-E`: disable backslash escape characters
- `cat`: print contents of a file
    - `-n`: print line numbers
    - `-b`: print line numbers, skipping empty lines 
    - `-s`: remove consecutive empty lines 
    - `-v`: show non-printing characters
    - `file1.txt file2.txt > combined.txt`: appends contents together into same file 
    - `file1.txt | grep "some_word"`: pipe operator `|` allows you to pipe contents to other commands
- `cp`: copy files and directories
    - `-r`: recursively copy
    - `-i`: interactive mode (ask before overwritting)
    - `-u`: copy only if the source is newer
    - `-v`: verbose mode
- `mv`: move files or rename them 
    - `-i`: interactive mode (ask before overwritting)
    - `-v`: verbose mode
    - `-u`: move only if source is newer
- `rm`: remove 
    - `-r`: recursively delete contents
    - `-i`: interactive mode (ask before deleting)
    - `-F`: force delete 
    - `-v`: verbose mode
- `tr {input} {output}`: translate, replaces all occurrences of input in stdin to output
- `touch`: changes file timestamps or creates an empty file if it does not exist 
    - `-a`: update only when file was last read
    - `-m`: update only when file was last changed
    - `-t`: set to specific time 
    - `-c`: do not create new files
- `mkdir`: make new directory 
    - `-p`: create parent directories
    - `-v`: verbose mode
    - `-m`: set file mode permissions for directory 
- `alias`: alias names to commands
    - `alias`: lists all aliases
    - `alias name='command'`: assign alias
    - `unalias name`: remove aliases

## File Pipeline Operators

- `{command} > {filename}`: takes stdout from the command and outputs to file (overwrite if it already exists)
- `{command} >> {filename}`: takes stdout from the command and outputs to file (appends if it already exists)
- `{command} 2> {filename}`: takes stderr from the command and outputs to file 
- `{command} &> {filename}`: takes both stdout and stderr from the command and output to file
- `{command} < {filename}`: takes contents from the file and outputs them to the stdin of the command
- `{command1} | {command2}`: takes stdout of command1 and outputs them to stdin of command2
- `{command1} |& {command2}`: takes stderr of command1 and outputs them to stdin of command2
- `{command} <<< {string}`: "here string", takes a string and pipes it into a command

## Basic Tools

- `grep {keyword} {filename}`: searches for keyword in filename or if filename is not specified then from stdin
    - `-A{n}`: searches n lines after the searched line
    - `-B{n}`: searches n lines before the searched line
    - `-C{n}`: context, searches n lines before and after the searched the line
- `less {filename}`: creates a pager for the filename or if filename is not specified then from stdin 
- `man`: bash manual
- `history`: lists out history of cmdline commands (usually want to just use CTRL+r for fzf command search)
- `file` {filename}: determines the file type of filename

## Variables

`var_name=var`: sets a variable `var` to be referenced by `var_name` within the context of the given shell session 

`"$var_name"`: gives the value of variable `varname` (double quotes surrounding returns original value)

`var_name=$(command)`: allows for the command output to be saved as `var_name`

`unset var_name`: removes the variable `varname`

# Scripting Basics 

## File Permissions

`ls -l`: command that lists contents of the directory in long format (note the first part represents the permissions)

`chmod +x {filename}`: "change mode", adds the executable bit into the file's access permissions

## Executing Scripts

`./{script}`: execute script in new shell environment 
`source {script}`: execute script in current shell environment
- Note: `. {script}` does the exact same thing

`#!/usr/bin/env bash`: a shebang ("hash+bang") that specifies which interpreter should run the file (specify at the top of every bash file)

## Core Scripting Concepts

**Loops**
```bash 
# for loop
for var in {array}; do 
    ...
done

# while loop
while [[ CONDITONAL_EXPRESSION ]]; do 
    ...
done

# until = opposite of while loop
until [[ CONDITONAL_EXPRESSION ]]; do 
    ...
done

# C-style for loops exist in bash using (()) = "math mode"
max=5
for ((i=0; i<max; i++)); do
    ...
done
```

**Passing in Arguments**
```bash
read -p "Some Random Prompt: " prompt_var
$1 # reads from first argument 
$@ # creates an array of all the arguments
```

**Conditionals**
```bash
if [[ CONDITONAL_EXPRESSION ]] ; then
    ...
else
    ...
fi

# case statements in bash == switch statements in python 
case $var in 
    var1) 
        ...
        ;; # match first and then break
    var2)
        ...
        ;& # keep falling through the follow cases w/o checking matches
    *)
        ...
        ;;& # check every single case and go in if it matches
esac
```
- Note: `[[ CONDITIONAL_EXPRESSION ]]` actually invokes the `test` command on the expression (see the operators for `test` command)
- `$?`: returns the return value of the last executed command
- `$#`: returns the number of arguments given

**Functions**
```bash
func_name(){
    ...
    return 0 # keyword that only works in a function 
}
func_name # uses the function `func_name`
```
- Note: functions still have stdin, stdout, and stderr like if they were separate executable scripts

**Indexed Arrays** 
```bash
array=(val1 val2 val3)
echo ${array} # val1, only returns the first element
echo ${array[1]} # val2, indexed element from array  
echo ${array[-1]} # val3, negative indicies go from back of array
echo ${array[@]} # val1 val2 val3, loops through all elements in the array
echo ${#array} # 3, length of the array
array+=val4 # appends val4 to the array
```

**Associative Arrays (Dicts)**
```bash
declare -A arr # sets the variable arr as an associative array 
arr[key1]=val1
arr[key2]=val2
arr[key3]=val3

echo ${arr[key1]} # val1, returns the value associated with the key
echo ${arr[@]} # val1 val2 val3, returns all the values of the associative array 
echo ${!arr[@]} # key1 key2 key3, returns all the keys of the associative array 
```

**Scoping**
```bash
# runs the code with local scope within a subshell (variables are unset after execution) 
(
    ...
)
```
- Note: this is useful for setting the IFS (Internal Field Separator) variable `IFS` which determines how words are separated and default set to `$' \t\n'`

## Surrounding Thingies

**Command Substition**
```bash
echo $(echo hello) # prints "hello" 
```
- `$(command)`: outputs the stdout of the command inside by running the command in a subshell process and return the stdout


**Arthmetic Expression**
```bash
# for loops 
for ((i=0; i<5; i++)); do
    ...
done

# numeric conditionals
if ((i > 5)); then 
    ...
fi

# increments
((i++))
```
- `((expression))`: allows for arthimetic expression in a C-style way 

**Process Substitution**
```bash
while read -r word; do 
    echo "$word" 
    (i++)
done < <(grep file) # this the process substitution and useful for streaming data
```
- `<(command)` takes the stdout of the command and saves it to intermediate folder that then gets consumed by the shell env that calls it