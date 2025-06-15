from backend.algorithms.algoAPI import stringMatching
from backend.database.operations import DatabaseOperations
# from backend.database.models import ApplicationDetail, ApplicantProfile
# from backend.utils.pdf_extract import extract_pdfs
from backend.utils.pdf_extract import extract_text
from datetime import datetime, date
import os

class SearchController:
    @staticmethod
    def extract_cv_texts():
        try:
            # print("Extracting CV texts from PDF files...")
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            project_root = os.path.dirname(project_root)
            applications = DatabaseOperations.get_all_applications()
            if not applications:
                print("No applications found in the database.")
                return None
            # print(f"Found {len(applications)} applications in the database.")

            dict_of_cv_texts = {}
            for app in applications:
                if app.cv_path:
                    # Construct the full path correctly
                    full_path = os.path.join(project_root, app.cv_path.replace('/', os.sep))
                    if os.path.exists(full_path):
                        # print(f"Processing: {full_path}")
                        try:
                            # Call extract_text directly instead of extract_pdfs
                            extracted_text = extract_text(full_path)
                            if extracted_text:
                                dict_of_cv_texts[full_path] = extracted_text
                                print(f"Successfully extracted text from {full_path}")
                        except Exception as e:
                            print(f"Error extracting {full_path}: {e}")
                    else:
                        print(f"CV path does not exist: {full_path}")

            print(f"Successfully extracted {len(dict_of_cv_texts)} CVs.")
            return dict_of_cv_texts

        except Exception as e:            
            print(f"Error in extract_cv_texts: {e}")
            return None
    
    @staticmethod
    def search_cvs(keywords: list[str], algorithm: int, top_n: int = None, dict_of_cv_texts: dict[str, str] = None):
        try:
            print(f"Searching for keywords: {keywords} using algorithm {algorithm}")
            search_results = stringMatching(keywords, algorithm, dict_of_cv_texts)
            if not search_results:
                return None
            final_output_results, exact_time, fuzzy_time, exact_count, fuzzy_count = search_results
            processed_results = []
            for cv_path, (counts, match_flags) in final_output_results.items():
                exact_matches = [(kw, count) for kw, count, flag in zip(keywords, counts, match_flags) if flag == 1 and count > 0]
                fuzzy_matches = [(kw, count) for kw, count, flag in zip(keywords, counts, match_flags) if flag == 2 and count > 0]
                if exact_matches or fuzzy_matches:
                    file_name = cv_path.split("Tubes3_ikandanpisang\\")[-1].replace('\\', '/')
                    app_details = DatabaseOperations.get_application_by_cv_path(file_name)
                    applicant_info = {}
                    if app_details:
                        applicant = DatabaseOperations.get_applicant_by_id(app_details.applicant_id)
                        if applicant:
                            try:
                                birth_date = "N/A"
                                if hasattr(applicant, 'date_of_birth') and applicant.date_of_birth:
                                    if isinstance(applicant.date_of_birth, (date, datetime)):
                                        birth_date = applicant.date_of_birth.strftime('%Y-%m-%d')
                                    else:
                                        birth_date = str(applicant.date_of_birth)
                            except Exception as e:
                                print(f"Error formatting date: {e}")
                                birth_date = "N/A"
                            applicant_info = {
                                "name": f"{applicant.first_name} {applicant.last_name}",
                                "role": app_details.application_role,
                                "phone": applicant.phone_number,
                                "address": applicant.address,
                                "dob": birth_date
                            }
                            name = applicant_info["name"]
                        else:
                            print(f"Applicant not found for CV: {cv_path}")
                            name = os.path.basename(cv_path).replace('.pdf', '')
                    else:
                        print(f"No application details found for CV: {cv_path}")
                        name = os.path.basename(cv_path).replace('.pdf', '')
                    
                    result = {
                        "name": name,
                        "exact_matches": exact_matches,
                        "fuzzy_matches": fuzzy_matches,
                        "total_matches": sum(count for _, count in exact_matches) + sum(count for _, count in fuzzy_matches),
                        "cv_path": cv_path,
                        "applicant_id": app_details.applicant_id if app_details else None,
                        "applicant_info": applicant_info,
                        "cv_txt": dict_of_cv_texts.get(cv_path, ""),
                    }
                    processed_results.append(result)
            processed_results.sort(key=lambda x: x["total_matches"], reverse=True)
            if top_n:
                processed_results = processed_results[:top_n]
            
            return {
                "results": processed_results,
                "statistics": {
                    "exact_time": exact_time,
                    "fuzzy_time": fuzzy_time,
                    "exact_processed": exact_count,
                    "fuzzy_processed": fuzzy_count,
                    "total_time": exact_time + fuzzy_time
                }
            }
                
        except Exception as e:
            print(f"Error in search_cvs: {e}")
            return None