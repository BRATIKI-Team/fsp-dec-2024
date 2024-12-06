import type { IEvent } from '~/types/dtos/event';

export default () => {
  const map_after_request = (item: IEvent) => ({
    ...item,
    datetime: new Date(item.datetime),
  });

  return {
    map_after_request,
  };
};
