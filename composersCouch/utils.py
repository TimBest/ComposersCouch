from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def get_page(page_num, item_list, items_per_page):
    paginator = Paginator(item_list, items_per_page)
    try:
        page = paginator.page(page_num)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        page = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        page = paginator.page(paginator.num_pages)
    return page

ALL_FIXTURES = [
    'users', 'profiles',
    'artists', 'members',
    'contactInfos', 'contacts', 'locations', 'zipcodes',
    'fans',
    'genres',
    'applications', 'numApplicants', 'privateRequests', 'publicRequests', 'requestParticipants',
    'calendars', 'dates',
    'participants', 'threads', 'messages',
    'albums',
    'venues',
]
