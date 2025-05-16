cd ..
file_labels="../repo_de_prueba/Toolkit/labelsGalatea.csv"
cd $VAR_NAME_ROOT_REPOSITORY/

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
cp -f "$VAR_NAME_ROOT_REPOSITORY/galatea/report_issue_galatea.yaml" "$VAR_NAME_ROOT_REPOSITORY/.github/ISSUE_TEMPLATE/report_issue.yaml"

#Add scripts python
cp "$VAR_NAME_ROOT_REPOSITORY/galatea/scripts"* "$VAR_NAME_ROOT_REPOSITORY/scripts/"

#Add actions
cp "$VAR_NAME_ROOT_REPOSITORY/galatea/workflows"* "$VAR_NAME_ROOT_REPOSITORY/.github/workflow/"

