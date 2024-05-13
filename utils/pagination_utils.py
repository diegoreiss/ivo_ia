from typing import Dict


class PaginationUtils:
    def paginate(self, list, page_size, page_number):
        start_index, end_index = self.__get_start_end_index(page_size, page_number)

        return {
            'page_data': list[start_index:end_index],
            'total_pages': self.__get_total_pages(list, page_size)
        } 
    
    def paginate_dict(self, dict: Dict, page_size, page_number):
        keys = list(dict.keys())

        start_index, end_index = self.__get_start_end_index(page_size, page_number)
        paginated_keys = keys[start_index:end_index]
        paginated_data = {key: dict[key] for key in paginated_keys}

        return {
            'page_data': paginated_data,
            'total_pages': self.__get_total_pages(keys, page_size)
        }
    
    def __get_start_end_index(self, page_size, page_number):
        start_index = (page_number - 1) * page_size
        end_index = start_index + page_size

        return start_index, end_index
        
    
    def __get_total_pages(self, list, page_size):
        return (len(list) + page_size - 1) // page_size
