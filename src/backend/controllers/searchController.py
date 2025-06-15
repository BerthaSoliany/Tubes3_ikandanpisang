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
            print("Extracting CV texts from PDF files...")
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            project_root = os.path.dirname(project_root)
            applications = DatabaseOperations.get_all_applications()
            if not applications:
                print("No applications found in the database.")
                return None
            print(f"Found {len(applications)} applications in the database.")

            dict_of_cv_texts = {}
            for app in applications:
                if app.cv_path:
                    # Construct the full path correctly
                    full_path = os.path.join(project_root, app.cv_path.replace('/', os.sep))
                    if os.path.exists(full_path):
                        print(f"Processing: {full_path}")
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
            print("cekkkkk -1")
            final_output_results, exact_time, fuzzy_time, exact_count, fuzzy_count = search_results
            print("cekkkkkkkk 0")
            processed_results = []
            for cv_path, (counts, match_flags) in final_output_results.items():
                exact_matches = [(kw, count) for kw, count, flag in zip(keywords, counts, match_flags) if flag == 1 and count > 0]
                fuzzy_matches = [(kw, count) for kw, count, flag in zip(keywords, counts, match_flags) if flag == 2 and count > 0]
                # print(f"Processing CV: {cv_path}")
                # print(f"Exact Matches: {exact_matches}")
                # print(f"Fuzzy Matches: {fuzzy_matches}")
                if exact_matches or fuzzy_matches:
                    # print("masuk bos")
                    file_name = cv_path.split("Tubes3_ikandanpisang\\")[-1].replace('\\', '/')
                    print(f"cekkkk 1")
                    app_details = DatabaseOperations.get_application_by_cv_path(file_name)
                    print(f"cekkkk 2")
                    applicant_info = {}
                    if app_details:
                        print("cekkk 3")
                        applicant = DatabaseOperations.get_applicant_by_id(app_details.applicant_id)
                        print ("cekkk 4")
                        if applicant:
                            try:
                                birth_date = "N/A"
                                print("haii")
                                if hasattr(applicant, 'date_of_birth') and applicant.date_of_birth:
                                    print("uuuuu")
                                    if isinstance(applicant.date_of_birth, (date, datetime)):
                                        print("masuk sini 2")
                                        birth_date = applicant.date_of_birth.strftime('%Y-%m-%d')
                                    else:
                                        print("masuk sini")
                                        birth_date = str(applicant.date_of_birth)
                            except Exception as e:
                                print(f"Error formatting date: {e}")
                                birth_date = "N/A"
                            print("aaaaaaaaaaaaa")
                            # print("cekkk" + applicant.date_of_birth)
                            applicant_info = {
                                "name": f"{applicant.first_name} {applicant.last_name}",
                                "role": app_details.application_role,
                                "phone": applicant.phone_number,
                                "address": applicant.address,
                                "dob": birth_date
                            }
                            print("cek apalah ini")
                            name = applicant_info["name"]
                            # print(f"Processing CV for applicant: {name}")
                            # print(f"CV Path: {cv_path}")
                            # print(f"Role: {app_details.application_role}")
                            # print(f"Phone: {applicant_info['phone']}")
                            # print(f"Address: {applicant_info['address']}")
                            # print(f"DOB: {applicant_info['dob']}")
                        else:
                            print(f"Applicant not found for CV: {cv_path}")
                            name = os.path.basename(cv_path).replace('.pdf', '')
                    else:
                        print(f"No application details found for CV: {cv_path}")
                        name = os.path.basename(cv_path).replace('.pdf', '')
                    
                    print(f"cekkk 5")
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
                    print(f"cekkk 6")
            processed_results.sort(key=lambda x: x["total_matches"], reverse=True)
            print("cekkk 7")
            if top_n:
                print("cekkkk 8")
                processed_results = processed_results[:top_n]
                print("cekkkkk 9")
            
            print("cekkkk 10")
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