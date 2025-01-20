from .documents import ClinicDocument, DentistDocument, CategoryDocument

def search_all(query):
   # Sử dụng truy vấn match_phrase để tìm kiếm chính xác
    clinic_search = ClinicDocument.search().query("match_phrase", clinic_name=query)
    clinic_results = clinic_search.execute()
    
    if clinic_results.hits.total.value == 0:
        # Nếu không tìm thấy kết quả, bạn có thể thực hiện một tìm kiếm khác hoặc xử lý theo cách khác
        clinic_search = ClinicDocument.search().query("multi_match", query=query, fields=['clinic_name', 'address', 'description'])
        clinic_results = clinic_search.execute()

    # Tìm kiếm trong Dentist
    dentist_search = DentistDocument.search().query("match_phrase", dentist_name=query)
    dentist_results = dentist_search.execute()

    # Nếu không tìm thấy kết quả, tìm kiếm mở rộng
    if dentist_results.hits.total.value == 0:
        dentist_search = DentistDocument.search().query("multi_match", query=query, fields=['dentist_name', 'specialization'])
        dentist_results = dentist_search.execute()

    # Tìm kiếm trong Category
    category_search = CategoryDocument.search().query("match_phrase", name=query)
    category_results = category_search.execute()

    # Nếu không tìm thấy kết quả, tìm kiếm mở rộng
    if category_results.hits.total.value == 0:
        category_search = CategoryDocument.search().query("multi_match", query=query, fields=['name'])
        category_results = category_search.execute()

    return {
        'clinics': clinic_results,
        'dentists': dentist_results,
        'categories': category_results
    }

# from .documents import ClinicDocument

# def search_all(query):
#     # Sử dụng truy vấn match_phrase để tìm kiếm chính xác
#     search = ClinicDocument.search().query("match_phrase", clinic_name=query)
#     response = search.execute()
    
#     if response.hits.total.value == 0:
#         # Nếu không tìm thấy kết quả, bạn có thể thực hiện một tìm kiếm khác hoặc xử lý theo cách khác
#         search = ClinicDocument.search().query("multi_match", query=query, fields=['clinic_name', 'address', 'description'])
#         response = search.execute()
    
#     return response
