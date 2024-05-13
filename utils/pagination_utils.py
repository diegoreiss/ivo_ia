class PaginationUtils:
    def paginate(self, list, page_size, page_number):
        start_index = (page_number - 1) * page_size
        end_index = start_index + page_size

        return {
            'page_data': list[start_index:end_index],
            'total_pages': self.__get_total_pages(list, page_size)
        } 
    
    def __get_total_pages(self, list, page_size):
        return (len(list) + page_size - 1) // page_size
