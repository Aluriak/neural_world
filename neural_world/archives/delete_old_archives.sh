rm -r $(ls | grep sim_ | sort | head -n -1) 2>/dev/null


if (( $? == 0 )); then
    echo 'Olds archives deleted.'
else
    echo 'Nothing to do.'
fi
