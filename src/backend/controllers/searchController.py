from backend.algorithms.algoAPI import stringMatching
from backend.database.operations import DatabaseOperations
# from backend.database.models import ApplicationDetail, ApplicantProfile
import os

class SearchController:
    @staticmethod
    def search_cvs(keywords: list[str], algorithm: int, top_n: int = None):
        try:
            print(f"Searching for keywords: {keywords} using algorithm {algorithm}")
            search_results = stringMatching(keywords, algorithm)
            if not search_results:
                return None
            
            final_output_results, exact_time, fuzzy_time, exact_count, fuzzy_count, dict = search_results
            
            processed_results = []
            for cv_path, (counts, match_flags) in final_output_results.items():
                exact_matches = [(kw, count) for kw, count, flag in zip(keywords, counts, match_flags) if flag == 1 and count > 0]
                fuzzy_matches = [(kw, count) for kw, count, flag in zip(keywords, counts, match_flags) if flag == 2 and count > 0]
                # print(f"Processing CV: {cv_path}")
                # print(f"Exact Matches: {exact_matches}")
                # print(f"Fuzzy Matches: {fuzzy_matches}")
                if exact_matches or fuzzy_matches:
                    # print("masuk bos")
                    cv_path = cv_path.split("Tubes3_ikandanpisang\\")[-1].replace('\\', '/')
                    app_details = DatabaseOperations.get_application_by_cv_path(cv_path)
                    
                    applicant_info = {}
                    if app_details:
                        applicant = DatabaseOperations.get_applicant_by_id(app_details.applicant_id)
                        if applicant:
                            applicant_info = {
                                "name": f"{applicant.first_name} {applicant.last_name}",
                                "role": app_details.application_role,
                                "phone": applicant.phone_number,
                                "address": applicant.address,
                                "dob": applicant.date_of_birth.strftime("%Y-%m-%d") if applicant.date_of_birth else None
                            }
                            name = applicant_info["name"]
                            print(f"Processing CV for applicant: {name}")
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
                    
                    result = {
                        "name": name,
                        "exact_matches": exact_matches,
                        "fuzzy_matches": fuzzy_matches,
                        "total_matches": sum(count for _, count in exact_matches) + sum(count for _, count in fuzzy_matches),
                        "cv_path": cv_path,
                        "applicant_id": app_details.applicant_id if app_details else None,
                        "applicant_info": applicant_info
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