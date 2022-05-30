## Installation Instructions

1. At the root of the directory, run `make infra`.
> NOTE: This leverages the Makefile to create the translator resource, and the storage containers for the document
translation demo. Key outputs are stored in a `variables.env` file. Before running this command, a `sub.env`
needs to be present in the root of the directory, with a single line as follows: `SUB_ID=<subscription>`.

2. Portal specific operations. While the focus is to automate creation of all resources and infra, there are
   two manual steps that need to be done in the Portal.
	- **Generate Custom Domain Name**. On the translator resource, ensure `Generate Custom Domain Name` is
	  not there. If it is, then click it, and provide the same translator resource name. Save this
	  operation since this will allow the Document Translation service to recognize this resource.
	- **Managed system identities.** To avoid having to generate multiple SAS tokens, ensure your
	  translator resource is setup with a managed system identity. For more details, refer this
	  documentation: https://docs.microsoft.com/en-us/azure/cognitive-services/translator/document-translation/managed-identity
   
3. The custom translation model is created in the Custom Translator Portal. For executing the sample demo
   instructions, you will need the specific `Category ID` of the custom model.

4. If running the demo commands in an ipython environment as opposed to a python environment, you may need to
   install the `requests` library and the `python-dotenv` library.
