import re
import os

def extract_ksbs_to_markdown(ksb_text: str, output_folder: str = "ksbs"):
    """
    Extracts KSBs (Knowledge, Skills, Behaviours) from a given text,
    and saves each KSB's description into a separate Markdown file.

    Args:
        ksb_text (str): The input text containing KSBs.
                        KSBs are expected to be formatted as K#, S#, or B#
                        followed by a colon (e.g., "K1:", "S5:", "B10:").
        output_folder (str): The name of the folder where Markdown files
                             will be saved. Defaults to "ksbs".
    """
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)
    print(f"Ensuring output directory '{output_folder}' exists...")

    # Regex to find KSB identifiers and capture the description that follows.
    # It looks for 'K', 'S', or 'B' followed by digits and a colon,
    # then captures everything non-greedily until the next KSB identifier
    # or the end of the string.
    # re.DOTALL allows '.' to match newlines.
    # The pattern is adjusted to use ':' instead of '.' as the separator.
    ksb_pattern = re.compile(r'(K\d+|S\d+|B\d+):\s*(.*?)(?=(?:K|S|B)\d+:|\Z)', re.DOTALL)

    matches = ksb_pattern.findall(ksb_text)
    
    if not matches:
        print("No KSBs found in the provided text. Please check the format (e.g., K1:, S5:, B10:).")
        return

    print(f"Found {len(matches)} KSBs. Processing...")

    for ksb_id, description in matches:
        # Clean up KSB ID for filename: convert to lowercase
        ksb_id_clean = ksb_id.strip().lower()
        
        # Strip leading/trailing whitespace from the description
        clean_description = description.strip()

        # Construct filename
        filename = os.path.join(output_folder, f"{ksb_id_clean}.desc.md")

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(clean_description)
            print(f"Created {filename}")
        except IOError as e:
            print(f"Error writing to file {filename}: {e}")

# --- Your KSB Text Goes Here ---
# This variable now contains the KSB text you provided.
ksb_text = """
K1: How to use AI and machine learning methodologies such as data-mining, supervised/unsupervised machine learning, natural language processing, machine vision to meet business objectives
K2: How to apply modern data storage solutions, processing technologies and machine learning methods to maximise the impact to the organisation by drawing conclusions from applied research
K3: How to apply advanced statistical and mathematical methods to commercial projects
K4: How to extract data from systems and link data from multiple systems to meet business objectives
K5: How to design and deploy effective techniques of data analysis and research to meet the needs of the business and customers
K6: How data products can be delivered to engage the customer, organise information or solve a business problem using a range of methodologies, including iterative and incremental development and project management approaches
K7: How to solve problems and evaluate software solutions via analysis of test data and results from research, feasibility, acceptance and usability testing
K8: How to interpret organisational policies, standards and guidelines in relation to AI and data
K9: The current or future legal, ethical, professional and regulatory frameworks which affect the development, launch and ongoing delivery and iteration of data products and services.
K10: How own role fits with, and supports, organisational strategy and objectives
K11: The roles and impact of AI, data science and data engineering in industry and society
K12: The wider social context of AI, data science and related technologies, to assess business impact of current ethical issues such as workplace automation and misuse of data
K13: How to identify the compromises and trade-offs which must be made when translating theory into practice in the workplace
K14: The business value of a data product that can deliver the solution in line with business needs, quality standards and timescales
K15: The engineering principles used (general and software) to investigate and manage the design, development and deployment of new data products within the business
K16: Understand high-performance computer architectures and how to make effective use of these
K17: How to identify current industry trends across AI and data science and how to apply these
K18: The programming languages and techniques applicable to data engineering
K19: The principles and properties behind statistical and machine learning methods
K20: How to collect, store, analyse and visualise data
K21: How AI and data science techniques support and enhance the work of other members of the team
K22: The relationship between mathematical principles and core techniques in AI and data science within the organisational context
K23: The use of different performance and accuracy metrics for model validation in AI projects
K24: Sources of error and bias, including how they may be affected by choice of dataset and methodologies applied
K25: Programming languages and modern machine learning libraries for commercially beneficial scientific analysis and simulation
K26: The scientific method and its application in research and business contexts, including experiment design and hypothesis testing
K27: The engineering principles used (general and software) to create new instruments and applications for data collection
K28: How to communicate concepts and present in a manner appropriate to diverse audiences, adapting communication techniques accordingly
K29: The need for accessibility for all users and diversity of user needs
Skills
S1: Use applied research and data modelling to design and refine the database & storage architectures to deliver secure, stable and scalable data products to the business
S2: Independently analyse test data, interpret results and evaluate the suitability of proposed solutions, considering current and future business requirements
S3: Critically evaluate arguments, assumptions, abstract concepts and data (that may be incomplete), to make recommendations and to enable a business solution or range of solutions to be achieved
S4: Communicate concepts and present in a manner appropriate to diverse audiences, adapting communication techniques accordingly
S5: Manage expectations and present user research insight, proposed solutions and/or test findings to clients and stakeholders.
S6: Provide direction and technical guidance for the business with regard to AI and data science opportunities
S7: Work autonomously and interact effectively within wide, multidisciplinary teams
S8: Coordinate, negotiate with and manage expectations of diverse stakeholders suppliers with conflicting priorities, interests and timescales
S9: Manipulate, analyse and visualise complex datasets
S10: Select datasets and methodologies most appropriate to the business problem
S11: Apply aspects of advanced maths and statistics relevant to AI and data science that deliver business outcomes
S12: Consider the associated regulatory, legal, ethical and governance issues when evaluating choices at each stage of the data process
S13: Identify appropriate resources and architectures for solving a computational problem within the workplace
S14: Work collaboratively with software engineers to ensure suitable testing and documentation processes are implemented.
S15: Develop, build and maintain the services and platforms that deliver AI and data science
S16: Define requirements for, and supervise implementation of, and use data management infrastructure, including enterprise, private and public cloud resources and services
S17: Consistently implement data curation and data quality controls
S18: Develop tools that visualise data systems and structures for monitoring and performance
S19: Use scalable infrastructures, high performance networks, infrastructure and services management and operation to generate effective business solutions.
S20: Design efficient algorithms for accessing and analysing large amounts of data, including Application Programming Interfaces (API) to different databases and data sets
S21: Identify and quantify different kinds of uncertainty in the outputs of data collection, experiments and analyses
S22: Apply scientific methods in a systematic process through experimental design, exploratory data analysis and hypothesis testing to facilitate business decision making
S23: Disseminate AI and data science practices across departments and in industry, promoting professional development and use of best practice
S24: Apply research methodology and project management techniques appropriate to the organisation and products
S25: Select and use programming languages and tools, and follow appropriate software development practices
S26: Select and apply the most effective/appropriate AI and data science techniques to solve complex business problems
S27: Analyse information, frame questions and conduct discussions with subject matter experts and assess existing data to scope new AI and data science requirements
S28: Undertakes independent, impartial decision-making respecting the opinions and views of others in complex, unpredictable and changing circumstances
Behaviours
B1: A strong work ethic and commitment in order to meet the standards required.
B2: Reliable, objective and capable of independent and team working
B3: Acts with integrity with respect to ethical, legal and regulatory ensuring the protection of personal data, safety and security
B4: Initiative and personal responsibility to overcome challenges and take ownership for business solutions
B5: Commitment to continuous professional development; maintaining their knowledge and skills in relation to AI developments that influence their work
B6: Is comfortable and confident interacting with people from technical and non-technical backgrounds. Presents data and conclusions in a truthful and appropriate manner
B7: Participates and shares best practice in their organisation, and the wider community around all aspects of AI data science
B8: Maintains awareness of trends and innovations in the subject area, utilising a range of academic literature, online sources, community interaction, conference attendance and other methods which can deliver business value
"""

# --- Run the script ---
if __name__ == "__main__":
    extract_ksbs_to_markdown(ksb_text)
    print("\nKSB extraction complete. Check the 'ksbs' folder for your files.")
