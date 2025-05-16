cd ..
rm -r repo_de_prueba
gh repo clone Fredesa/repo_de_prueba
file_labels="../repo_de_prueba/Toolkit/labelsGalatea.csv"

cat "$file_labels" | while IFS= read -r line;
do
   if [[ $line != "" ]];
   then
    IFS_antiguo=$IFS
    IFS=";" 
    read -ra partes <<< "$line"
    IFS=$IFS_antiguo
    gh label create "${partes[0]}" --description "${partes[1]}" --color "${partes[2]}" -f
    echo "${partes[0]}"
   fi
done
#Update template issue
mkdir -p $VAR_NAME_ROOT_REPOSITORY/.github/ISSUE_TEMPLATE/
cp "galatea/report_issue_galatea.yaml" "$VAR_NAME_ROOT_REPOSITORY/.github/ISSUE_TEMPLATE/report_issue.yaml"

#Add scripts python
mkdir -p $VAR_NAME_ROOT_REPOSITORY/scripts/
cp "galatea/scripts/"* "$VAR_NAME_ROOT_REPOSITORY/scripts/"

#Add actions
mkdir -p $VAR_NAME_ROOT_REPOSITORY/.github/workflow/
cp "galatea/workflows/"* "$VAR_NAME_ROOT_REPOSITORY/.github/workflow/"

