from typing import Any
import aiohttp
import ujson


class Request:
    __base_url = None

    @property
    async def base_url(self):
        if isinstance(self.__base_url, str):
            return self.__base_url
        if self.__base_url.__class__.__name__ == 'function':
            url = self.__base_url()
            if url.__class__.__name__ == 'coroutine':
                return await url
            return url

    @base_url.setter
    def base_url(self, base_url):
        self.__base_url = base_url

    async def __call__(
            self,
            method: str, url: str,
            *,
            params: dict[str, Any] = None, body: dict[str, Any] = None, headers: dict[str, Any] = None,
            data: dict[str, Any] = None
    ) -> Any:
        assert (method := method.lower()) in ('get', 'post', 'put', 'delete')
        async with aiohttp.ClientSession(base_url=await self.base_url, json_serialize=ujson.dumps) as session:
            # convert params values to str
            for key, value in params.items() if params else {}:
                params[key] = str(value)
            request_method = getattr(session, method)
            async with request_method(url, json=body, params=params, headers=headers, data=data) as response:
                return await response.json()


request = Request()
