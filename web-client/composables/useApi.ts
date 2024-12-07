import useEvents from '~/composables/useEvents';
import useHelpers from '~/composables/useHelpers';
import type {
  IEvent,
  IEventCreateRequest,
  IEventDetail,
} from '~/types/dtos/event';
import type { IEventRequest } from '~/types/dtos/event_request';
import type { IMemberRequest } from '~/types/dtos/member_request';
import type { IRegion } from '~/types/dtos/region';
import type {
  ForgetPasswordRequest,
  ResetPasswordRequest,
} from '~/types/dtos/reset';
import type { ISearchRequest, ISearchResponse } from '~/types/dtos/search';
import { UserRole } from '~/types/dtos/user';
import type { User } from 'next-auth';

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

  const member_reqs_all = (region: string) =>
    $fetch<readonly IMemberRequest[]>(
      helpers_api.REQUEST_URL(`/member-reqs/${region}`),
      {
        method: 'GET',
        headers: helpers_api.AUTH_HEADERS(),
      }
    );

  const password_reset = (request: ResetPasswordRequest) =>
    $fetch<void>(helpers_api.REQUEST_URL(`/users/reset`), {
      method: 'PUT',
      body: request,
      headers: helpers_api.AUTH_HEADERS(),
    });

  const password_forget = (request: ForgetPasswordRequest) =>
    $fetch<void>(helpers_api.REQUEST_URL(`/users/forget`), {
      method: 'PUT',
      body: request,
      headers: helpers_api.AUTH_HEADERS(),
    });

  const download_file = (id: string) =>
    $fetch<void>(helpers_api.REQUEST_URL(`/files/${id}/download`), {
      method: 'GET',
      headers: helpers_api.AUTH_HEADERS(),
    });

  const member_reqs_change_status = (req: string, status: string) =>
    $fetch<readonly IMemberRequest[]>(
      helpers_api.REQUEST_URL(`/member-reqs/${req}/set-status/${status}`),
      {
        method: 'POST',
        headers: helpers_api.AUTH_HEADERS(),
      }
    );

  const region_update = async (id: string, body: IRegion) =>
    $fetch<IRegion>(helpers_api.REQUEST_URL(`/regions/${id}`), {
      method: 'PUT',
      body: body,
      headers: helpers_api.AUTH_HEADERS(),
    });

  const region_search = (request: ISearchRequest) =>
    $fetch<ISearchResponse<IRegion>>(
      helpers_api.REQUEST_URL('/regions/search'),
      {
        method: 'POST',
        body: request,
        headers: helpers_api.AUTH_HEADERS(),
      }
    );

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
      requests: {
        all: async () =>
          $fetch<Array<IEventRequest>>(
            helpers_api.REQUEST_URL('/event-requests/list-all'),
            {
              method: 'GET',
              headers: helpers_api.AUTH_HEADERS(),
            }
          ),
        change_status: async (
          req: string,
          body: {
            id: string;
            event_id: string;
            region_id: string;
            status: string;
            canceled_reason: string;
          }
        ) =>
          $fetch(helpers_api.REQUEST_URL(`/event-requests/${req}/set-status`), {
            method: 'POST',
            body: body,
            headers: helpers_api.AUTH_HEADERS(),
          }),
      },
    },
    regions: {
      all: regions_all,
      find: region_by_id,
      update: region_update,
      assign: async (region: string, role: string, user: string) =>
        $fetch<{id: string}>(helpers_api.REQUEST_URL(`/regions/${region}/assign-${role}/${user}`), {
          method: 'POST',
          headers: helpers_api.AUTH_HEADERS(),
        }),
      create: async (data: any) =>
        $fetch<{id: string}>(helpers_api.REQUEST_URL("/regions/create"), {
          method: 'POST',
          body: data,
          headers: helpers_api.AUTH_HEADERS(),
        }),
      search: region_search,
    },
    member_reqs: {
      all: member_reqs_all,
      change_status: member_reqs_change_status,
    },
    disciplines: {
      all: disciplines_all,
    },
    requests: {
      create: event_request_create,
    },
    auth: {
      register: async (body: {email: string, password: string}) =>
        $fetch<{id: string}>(helpers_api.REQUEST_URL('/users/register'), {
          method: 'POST',
          body: body,
          headers: helpers_api.AUTH_HEADERS(),
        }),
      reset: password_reset,
      forget: password_forget,
    },
    files: {
      download: download_file,
    },
  };
};
