---
title: Glossary
description: Key terms and definitions used in the Cohort Discovery Service documentation
tags:
  - reference
  - glossary
---

# Glossary

Definitions of key terms used throughout the Cohort Discovery Service documentation.

---

`BC|INSIGHT`
:   Query retrieval software developed by BC Platforms. One of the supported options for connecting a Custodian's OMOP data to the Cohort Discovery Service. Proprietary — contact BC Platforms directly for installation and support.

`BC|RQUEST`
:   A tool developed by BC Platforms that was previously used as the Cohort Discovery Service provider. Superseded by the current Cohort Discovery Service architecture.

`BC Platforms`
:   A global company based in the UK providing a modular data and technology platform for federated healthcare data, personalised medicine, and drug development. Developers of BC|INSIGHT.

`Bunny`
:   An open-source application developed by the University of Nottingham that supports Cohort Discovery. Bunny fetches Cohort Discovery queries and resolves them against an OMOP database. It is deployed locally and makes only outgoing requests, enabling safe execution behind a firewall. Supports obfuscation and federated networks via Hutch Relay. See [hutch.health/bunny/quickstart](https://hutch.health/bunny/quickstart).

`CO-CONNECT`
:   **Curated and Open aNalysis aNd rEsearCh plaTform**. A research project that set up the initial Cohort Discovery infrastructure and service (ended October 2022). The service was subsequently integrated into the Health Data Research Gateway.

`Carrot-Mapper`
:   **CaRROT-Mapper**. A web-tool that enables the mapping of a White Rabbit Scan Report to OMOP CDM, generating a JSON Mapping File that defines the ETL guidelines for the dataset. See [carrot4omop.ac.uk/Carrot-Mapper](https://carrot4omop.ac.uk/Carrot-Mapper/).

`Carrot-CDM`
:   An ETL tool that automates the extraction of pseudonymised data, transformation to OMOP CDM, and loading to Bunny or a similar query tool. See [carrot4omop.ac.uk/CaRROT-CDM](https://carrot4omop.ac.uk/CaRROT-CDM/).

`Data Controller`
:   The natural or legal person, public authority, agency, or other body which, alone or jointly with others, determines the purposes and means of the processing of personal data. Responsible for complying with GDPR and demonstrating compliance with data protection principles.

`Data Curation`
:   The organisation and integration of data collected from various sources.

`Data Custodian`
:   An organisation onboarding federated data into the Cohort Discovery Service. Responsible for the safe custody, transport, and storage of the data, as well as implementing business rules and maintaining the technical environment and database structure.

`Data Dictionary`
:   Information about data such as table and field descriptions, relationships to other data, origin, usage, and format.

`Data Discovery`
:   The process of obtaining actionable information by finding patterns in data from multiple sources.

`Data Governance`
:   Managing data assets throughout their lifecycle to ensure they meet organisational quality, integrity, and confidentiality standards.

`Data Interoperability`
:   The ability of systems and services that create, exchange, and consume data to have clear, shared expectations for the contents, context, and meaning of that data.

`Data Processor`
:   A natural or legal person, public authority, agency, or other body which processes personal data on behalf of a Data Controller.

`Dataset`
:   A collection of data. In tabular form, a dataset corresponds to one or more database tables, where every column represents a particular variable and each row corresponds to a given record.

`DPIA`
:   **Data Protection Impact Assessment**. A process to identify and assess project data risks. Data Custodians are **not required** to complete a DPIA for participation in the Cohort Discovery Service. If one is carried out, it would typically return that GDPR does not apply given the anonymisation and controls in place.

`ETL`
:   **Extract Transform Load**. A type of data integration that refers to the three steps used to combine data from multiple sources into a destination system in a different format. Preparation is supported by White Rabbit and Carrot Mapper.

`GDPR`
:   **General Data Protection Regulation**. A legal framework that sets guidelines for the collection and processing of personal information from individuals in the EU and UK.

`HDR UK`
:   **Health Data Research UK**. The UK national institute of Health Data Research. Mission: unite the UK's health and care data to enable discoveries that improve people's lives by providing scalable and robust data infrastructure and services. See [hdruk.ac.uk](https://www.hdruk.ac.uk).

`The Gateway`
:   **The Health Data Research Gateway**. The portal at [healthdatagateway.org](https://healthdatagateway.org) where researchers can search, discover, and request access to datasets, tools, and resources for research purposes.

`Metadata`
:   Information about the data. Two types are referenced in this documentation: (1) **Structural Metadata** — information about table names and field names in each dataset; (2) **Descriptive Metadata** — information for identification such as title, abstract, author, and keywords.

`OHDSI`
:   **Observational Health Data Sciences and Informatics** (pronounced "Odyssey"). A multi-stakeholder, interdisciplinary collaborative that enhances the value of health data through large-scale analytics. Current owners and developers of the OMOP Common Data Model.

`OMOP CDM`
:   **Observational Medical Outcomes Partnership — Common Data Model**. Allows for systematic analysis of disparate observational databases by transforming data into a common format and representation. Enables the capture of information (encounters, patients, providers, diagnoses, therapeutics, measurements, procedures) in the same way across different institutions.

`Pseudonymisation`
:   Defined within GDPR as "the processing of personal data in such a way that the data can no longer be attributed to a specific data subject without the use of additional information, as long as such additional information is kept separately and subject to technical and organisational measures to ensure non-attribution to an identified or identifiable individual."

`ScanReport`
:   The output file from a White Rabbit scan. Contains information on tables, values, field types, and data frequencies from a source dataset. Used as input to Carrot Mapper for OMOP mapping.

`SDE`
:   **Secure Data Environment**. Established by the NHS in England in 2024 to provide secure access to healthcare data for approved research projects. Allow approved users to access and analyse data without the data leaving the environment.

`SH / Safe Haven`
:   An alternate term for **Trusted Research Environment (TRE)**. Terms may be used interchangeably.

`Structural Mapping`
:   The (often manual) process of mapping source data tables and fields to OMOP CDM tables and fields.

`SSH`
:   **Secure Shell**. A secure remote management protocol that allows network services to be operated over an unsecured connection.

`Term Mapping`
:   The process of mapping source field values from one database to standard OMOP vocabulary.

`TRE`
:   **Trusted Research Environment**. Highly secure spaces for researchers accessing sensitive data. Based on the principle that researchers access and use data within a single secure environment — the data resides in one secure location and researchers interrogate it from there, with no data movement.

`Virtual Machine (VM)`
:   A computer resource that uses software instead of a physical computer to run programs and deploy applications. Multiple VMs can run on one physical host, each running its own operating system and functioning separately.

`White Rabbit`
:   A Java tool developed by OHDSI to help prepare ETLs of longitudinal healthcare databases into the OMOP CDM. The main function is to scan source data and provide detailed information on tables, fields, and values. Typically the first tool used in the ETL process.
