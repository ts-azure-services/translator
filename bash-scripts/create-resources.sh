#!/bin/bash
#Script to provision Cognitive Services account
grn=$'\e[1;32m'
end=$'\e[0m'

# Start of script
SECONDS=0

# Source subscription ID, and prep config file
source sub.env
sub_id=$SUB_ID

# Set the default subscription 
az account set -s $sub_id

# Create the resource group, location
number=$[ ( $RANDOM % 100000 ) + 1 ]
resourceGroup='cs'$number
translatorService='cs'$number'translator'
storageAccountName='sa'$number
sourceContainer='sourcedocs'
targetContainer='targetdocs'
location='westus2'

printf "${grn}STARTING CREATION OF RESOURCE GROUP...${end}\n"
rgCreate=$(az group create --name $resourceGroup --location $location)
printf "Result of resource group create:\n $rgCreate \n"

## Create translator text service
printf "${grn}CREATING THE TRANSLATOR TEXT SERVICE...${end}\n"
textTranslatorCreate=$(az cognitiveservices account create \
	--name $translatorService \
	-g $resourceGroup \
	--kind 'TextTranslation' \
	--sku S1 \
	--location $location)
printf "Result of text translator create:\n $textTranslatorCreate \n"

## Retrieve translator key 
printf "${grn}RETRIEVE KEYS & ENDPOINTS FOR SPEECH AND TRANSLATOR SERVICE...${end}\n"
translatorKey=$(az cognitiveservices account keys list -g $resourceGroup --name $translatorService --query "key1")
translatorLocation=$(az cognitiveservices account show -g $resourceGroup --name $translatorService --query "location")

printf "${grn}STARTING CREATION OF STORAGE ACCOUNT...${end}\n"
storageAccountCreate=$(az storage account create -n $storageAccountName \
	-g $resourceGroup\
	-l $location \
	--sku Standard_LRS)
printf "Result of storage account create:\n $storageAccountCreate\n"
sleep 7

printf "${grn}GET STORAGE ACCOUNT KEY...${end}\n"
storageAccountKey=$(az storage account keys list --account-name $storageAccountName \
	--query "[].{keys:value}[0].keys")

# Create the source container
printf "${grn}CREATE SOURCE CONTAINER...${end}\n"
sourceContainerCreate=$(az storage container create -n $sourceContainer \
	--account-name $storageAccountName \
	--account-key $storageAccountKey)
printf "Result of source container create:\n $sourceContainerCreate\n"

# Create the target container
printf "${grn}CREATE TARGET CONTAINER...${end}\n"
targetContainerCreate=$(az storage container create -n $targetContainer \
	--account-name $storageAccountName \
	--account-key $storageAccountKey)
printf "Result of target container create:\n $targetContainerCreate\n"

# Upload a file to source container, by first creating a SAS token
printf "${grn}CREATE SAS TOKEN TO UPLOAD TO BLOB...${end}\n"
sas_upload_blob=$(az storage container generate-sas \
	-n $sourceContainer \
	--account-name $storageAccountName \
	--account-key $storageAccountKey \
	--https-only \
	--permissions "dlrw")

# Need a write access SAS token to upload sample document
printf "${grn}UPLOAD FILE TO BLOB...${end}\n"
blobUpload=$(az storage blob upload -n "DemoDocument.docx" \
	--account-name $storageAccountName \
	--account-key $storageAccountKey \
	-c $sourceContainer \
	-f "./data-files/document_translation/DemoDocument.docx" \
	--sas-token $sas_upload_blob \
	--overwrite)
printf "Result of blob upload:\n $blobUpload\n"

## Generate read policy SAS token to source container
#printf "${grn}SAS TOKEN FOR READ FROM SOURCE...${end}\n"
#sas_read_source=$(az storage container generate-sas \
#	-n $sourceContainer \
#	--account-name $storageAccountName \
#	--account-key $storageAccountKey \
#	--https-only \
#	--permissions "lr")
##echo -ne "Result of SAS READ SOURCE TOKEN:\n $sas_read_source\n"

## Remove double quotes
#sas_read_source_modified=$(sed -e 's/^"//' -e 's/"$//' <<<"$sas_read_source")
#sourceContainerURL='https://'$storageAccountName'.blob.core.windows.net/'$sourceContainer'?'$sas_read_source_modified
sourceContainerURL='https://'$storageAccountName'.blob.core.windows.net/'$sourceContainer

## Generate write policy SAS token to target container
#printf "${grn}SAS TOKEN FOR WRITE FROM SOURCE...${end}\n"
#sas_write_target=$(az storage container generate-sas \
#	-n $targetContainer \
#	--account-name $storageAccountName \
#	--account-key $storageAccountKey \
#	--https-only \
#	--permissions "lw")
##echo -ne "Result of SAS WRITE TARGET TOKEN:\n $sas_write_target\n"

## Remove double quotes
#sas_write_target_modified=$(sed -e 's/^"//' -e 's/"$//' <<<"$sas_write_target")
##echo -ne "Result of SAS WRITE TARGET TOKEN modified...:\n $sas_write_target_modified\n"
#targetContainerURL='https://'$storageAccountName'.blob.core.windows.net/'$targetContainer'?'$sas_write_target_modified
targetContainerURL='https://'$storageAccountName'.blob.core.windows.net/'$targetContainer

# Create environment file for endpoints and keys
printf "${grn}WRITING OUT ENVIRONMENT VARIABLES...${end}\n"
configFile='variables.env'
printf "RESOURCE_GROUP=$resourceGroup \n"> $configFile
printf "TRANSLATOR_NAME=$translatorService \n">> $configFile
printf "TRANSLATOR_KEY=$translatorKey \n">> $configFile
printf "TRANSLATOR_LOCATION=$translatorLocation \n">> $configFile
printf "STORAGE_ACCT_KEY=$storageAccountKey \n">> $configFile
echo -ne "SOURCE_URL=$sourceContainerURL \n">> $configFile
echo -ne "TARGET_URL=$targetContainerURL \n">> $configFile

printf "${grn}GREAT JOB. INFRA ALL SETUP.........${end}\n"
sleep 10 # just to give time for artifacts to settle in the system, and be accessible
