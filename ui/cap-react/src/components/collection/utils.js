export const _getList = results => {
  return {
    drafts: {
      all: {
        list: results.drafts.data,
        more: results.drafts.more
      },
      yours: {
        list: results.user_drafts.data,
        more: results.user_drafts.more
      }
    },
    published: {
      all: {
        list: results.published.data,
        more: results.published.more
      },
      yours: {
        list: results.user_published.data,
        more: results.user_published.more
      }
    }
  };
};
