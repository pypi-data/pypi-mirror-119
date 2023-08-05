# Machina SDK Release 2.1.2

## Introduction
Welcome to the 2.1.2 release of the Machina SDK.  This release contains a few minor bug fixes.

Details are summarized below.

## New Features / Improvements

### Metadata Collector API for environment variables and network info
The AgentMetadataCollectorProcessEnvironment and AgentMetadataCollectorNetwork classes collect 
metadata from the environment variables and network identifiers respectively. Call getMetadata() on 
the collector and pass the results into the new addMetadata() function available on metadata holders,
like the Agent class.

### Change to return codes on loadProfiles
Previously, a missing file did not return an error. Now this function returns ISAGENT_RESOURCE_NOT_FOUND
unless called indirectly from an Agent intializer where a specific persistor file was not passed.

### Extended API for validating assertions
Previously, you could only use this API with a KNS server. You can now pass an enrollment URL instead.

## Issues Addressed
- Encrypt and Decrypt in place normally encrypt to a temporary file and then on success, delete the 
original file and rename the temp into its place. This breaks hard links in the file system, so now, 
if a file has hard links, it is now copied to a temp file and then encrypted/decrypted over the 
original file, which maintains the hard link.
- Validate assertion API did not correctly adjust for Daylight Savings Time.
- Removed a confusing log message when a key create encounters an HTTP error code.
- The default Linux persistor was not exposed in certain SDK wrappers.
- The Linux Key Vault was not exposed in certain SDK wrappers.
- Windows security fixes
  
## Discontinued Support
- None

## Additional Notes
- None

## Supported Platforms
The Machina SDK is tested against the following platform configurations:

|Platform    |Version                     |
|------------|----------------------------|
|Linux       | CentOS 7.8-2003            |
|Linux       | Ubuntu 18.04               |
|Windows     | Windows 8.1 (32 and 64 bit)|
|Windows     | Windows 10 (32 and 64 bit) |
|macOS       | macOS 13 (High Sierra)     |
|macOS       | macOS 14 (Mojave)          |
|macOS       | macOS 15 (Catalina)        |
|Python      | 3.8.x                      |
