import useEvents from '~/composables/useEvents';
import useHelpers from '~/composables/useHelpers';
import type {
  IEvent,
  IEventCreateRequest,
  IEventDetail,
} from '~/types/dtos/event';
import type { IRegion } from '~/types/dtos/region';
import type { ISearchRequest, ISearchResponse } from '~/types/dtos/search';

export default () => {
  const events_api = useEvents();
  const helpers_api = useHelpers();

  const events_search = (request: ISearchRequest) =>
    $fetch<ISearchResponse<IEventDetail>>(
      helpers_api.REQUEST_URL('/events/search'),
      {
        method: 'POST',
        body: request,
        headers: helpers_api.AUTH_HEADERS(),
      }
    ).then(response => ({
      ...response,
      items: response.items.map(item =>
        events_api.map_detail_after_request(item)
      ),
    }));

  const event_by_id = (id: string) =>
    $fetch<IEventDetail>(helpers_api.REQUEST_URL(`/events/${id}`), {
      method: 'GET',
      headers: helpers_api.AUTH_HEADERS(),
    }).then(response => ({
      ...events_api.map_detail_after_request(response),
    }));

  const event_request_create = (event_id: string) =>
    $fetch(
      helpers_api.REQUEST_URL(`/event-requests/${event_id}/send_request`),
      {
        method: 'POST',
        headers: helpers_api.AUTH_HEADERS(),
      }
    );

  const regions_all = () =>
    $fetch<readonly IRegion[]>(helpers_api.REQUEST_URL('/regions/get-all'), {
      method: 'GET',
      headers: helpers_api.AUTH_HEADERS(),
    });

  const region_by_id = (id: string) =>
    $fetch<IRegion>(helpers_api.REQUEST_URL(`/regions/${id}`), {
      method: 'GET',
      headers: helpers_api.AUTH_HEADERS(),
    });

  const disciplines_all = () =>
    $fetch<readonly string[]>(helpers_api.REQUEST_URL('/events/disciplines'), {
      method: 'GET',
      headers: helpers_api.AUTH_HEADERS(),
    });

  return {
    events: {
      search: events_search,
      create: async (body: IEventCreateRequest) =>
        $fetch<IEvent>(helpers_api.REQUEST_URL('/events'), {
          method: 'POST',
          body: body,
          headers: helpers_api.AUTH_HEADERS(),
        }),
      update: async (id: string, body: IEventCreateRequest) =>
        $fetch<IEvent>(helpers_api.REQUEST_URL(`/events/${id}`), {
          method: 'PUT',
          body: body,
          headers: helpers_api.AUTH_HEADERS(),
        }),
      find: event_by_id,
    },
    regions: {
      all: regions_all,
      find: region_by_id,
    },
    disciplines: {
      all: disciplines_all,
    },
    requests: {
      create: event_request_create,
    },
  };
};
