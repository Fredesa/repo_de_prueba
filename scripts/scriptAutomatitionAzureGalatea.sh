cd ..
rm -r repo_de_prueba
gh repo clone Fredesa/repo_de_prueba

file_labels="../repo_de_prueba/Toolkit/labelsGalatea.csv"
ls .
cd repo_de_prueba/

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
cp -n "repo_de_prueba/galatea/report_issue_galatea.yaml" "$VAR_NAME_ROOT_REPOSITORY/.github/ISSUE_TEMPLATE/report_issue.yaml"

#Add scripts python
cp -n "repo_de_prueba/galatea/scripts"* "$VAR_NAME_ROOT_REPOSITORY/scripts/"

#Add actions
cp -n"repo_de_prueba/galatea/workflows"* "$VAR_NAME_ROOT_REPOSITORY/.github/workflow/"

