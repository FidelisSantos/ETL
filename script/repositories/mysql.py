from typing import Any, Dict, List, Optional
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker, AsyncEngine
from sqlalchemy import text
from _types import ReportParams, FileParams

class MysqlRepository:
    def __init__(self, url: str, client: str):
        self.url = url
        self.client = client
        self._engine: Optional[AsyncEngine] = None
        self._session_factory: Optional[async_sessionmaker] = None

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    def _get_base_report_query(self) -> str:
        return """
        JSON_OBJECT('id', f.id, 'original_name', f.original_name) AS file,
        JSON_OBJECT('id', c.id, 'name', c.name) AS company,
        JSON_OBJECT('id', o.id, 'name', o.name) AS organization,
        CASE 
            WHEN ANY_VALUE(w.id) IS NULL THEN NULL
            ELSE JSON_OBJECT('id', ANY_VALUE(w.id), 'name', ANY_VALUE(w.name))
        END AS workstation,
        :client AS client
        """

    def _get_base_report_joins(self) -> str:
        return """
        JOIN companies c ON f.company_id = c.id
        JOIN organizations o ON f.organization_id = o.id
        JOIN workstations w ON f.workstation_id = w.id
        """

    def _get_engine(self) -> AsyncEngine:
        if self._engine is None:

            async_url = self.url.replace("mysql+pymysql://", "mysql+aiomysql://")
            self._engine = create_async_engine(async_url, future=True)
        return self._engine

    def _get_session_factory(self) -> async_sessionmaker:
        if self._session_factory is None:
            engine = self._get_engine()
            self._session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
        return self._session_factory

    async def _fetchall(self, query: str, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        session_factory = self._get_session_factory()
        async with session_factory() as session:
            result = await session.execute(text(query), params or {})
            rows = []
            for row in result:
                rows.append(dict(row._mapping))
            return rows

    async def _fetchone(self, query: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        rows = await self._fetchall(query, params)
        return rows[0] if rows else None

    async def close(self):
        if self._engine:
            await self._engine.dispose()

    # REBA
    def _get_base_reba_query(self) -> str:
        return f"""
        SELECT
            r.*,
            'REBA' AS type,
            :client AS client,
            {self._get_base_report_query()}
        FROM reba_reports r
        JOIN files f ON r.file_id = f.id
        {self._get_base_report_joins()}
        """
    async def get_reba(self, params: ReportParams) -> List[Dict[str, Any]]:
        query = f"""
        {self._get_base_reba_query()}
        WHERE 
            r.updated_at >= :start_date
            AND r.updated_at <= :end_date
        """
        return await self._fetchall(
            query,
            params={
                "client": self.client,
                "start_date": params["start_date"],
                "end_date": params["end_date"]
            }
        )

    async def get_realtime_reba(self) -> List[Dict[str, Any]]:
        query = f"""
        {self._get_base_reba_query()}
        WHERE
            r.updated_at >= NOW() - INTERVAL 1 YEAR;
        """
        return await self._fetchall(query, {"client": self.client})

    # KIM PUSH PULL
    def _get_base_kim_push_pull_query(self) -> str:
        return f"""
        SELECT
            kpp.*,
            'KIM_PP' AS type,
            {self._get_base_report_query()}
        FROM kim_push_pull_reports kpp
        JOIN files f ON kpp.file_id = f.id
        {self._get_base_report_joins()}
        """
    
    async def get_kim_push_pull(self, params: ReportParams) -> List[Dict[str, Any]]:
        query = f"""
        {self._get_base_kim_push_pull_query()}
        WHERE
            kpp.updated_at >= :start_date
            AND kpp.updated_at <= :end_date
        """
        return await self._fetchall(
            query,
            params={
                "client": self.client,
                "start_date": params["start_date"],
                "end_date": params["end_date"]
            }
        )

    async def get_realtime_kim_push_pull(self) -> List[Dict[str, Any]]:
        query = f"""
        {self._get_base_kim_push_pull_query()}
        WHERE
            kpp.updated_at >= NOW() - INTERVAL 1 YEAR;
        """
        return await self._fetchall(query, {"client": self.client})

    # STRAIN INDEX
    def _get_base_strain_index_query(self) -> str:
        return f"""
        SELECT
            si.*,
            'STRAIN_INDEX' AS type,
            {self._get_base_report_query()}
        FROM strain_index_reports si
        JOIN files f ON si.file_id = f.id
        {self._get_base_report_joins()}
        """
    async def get_strain_index(self, params: ReportParams) -> List[Dict[str, Any]]:
        query = f"""
        {self._get_base_strain_index_query()}
        WHERE
            si.updated_at >= :start_date
            AND si.updated_at <= :end_date
        """

        return await self._fetchall(
            query,
            params={
                "client": self.client,
                "start_date": params["start_date"],
                "end_date": params["end_date"]
            }
        )

    async def get_realtime_strain_index(self) -> List[Dict[str, Any]]:
        query = f"""
        {self._get_base_strain_index_query()}
        WHERE
            si.updated_at >= NOW() - INTERVAL 1 YEAR;
        """
        return await self._fetchall(query, {"client": self.client})

    # NIOSH
    def _get_base_niosh_query(self) -> str:
        return f"""
        SELECT
            n.*,
            'NIOSH' AS type,
            {self._get_base_report_query()}
        FROM niosh_reports n
        JOIN files f ON n.file_id = f.id
        {self._get_base_report_joins()}
        """
    async def get_niosh(self, params: ReportParams) -> List[Dict[str, Any]]:
        query = f"""
        {self._get_base_niosh_query()}
        WHERE
            n.updated_at >= :start_date
            AND n.updated_at <= :end_date
        """
        return await self._fetchall(
            query,
            params={
                "client": self.client,
                "start_date": params["start_date"],
                "end_date": params["end_date"]
            }
        )

    async def get_realtime_niosh(self) -> List[Dict[str, Any]]:
        query = f"""
        {self._get_base_niosh_query()}
        WHERE
            n.updated_at >= NOW() - INTERVAL 1 DAY;
        """
        return await self._fetchall(query, {"client": self.client})
    
    # KIM MHO
    def _get_base_kim_mho_query(self) -> str:
        return f"""
        SELECT
            kmho.*,
            'KIM_MHO' AS type,
            {self._get_base_report_query()}
        FROM kim_mho_reports kmho
        JOIN files f ON kmho.file_id = f.id
        {self._get_base_report_joins()}
        """

    async def get_kim_mho(self, params: ReportParams) -> List[Dict[str, Any]]:
        query = f"""
        {self._get_base_kim_mho_query()}
        WHERE
            kmho.updated_at >= :start_date
            AND kmho.updated_at <= :end_date
        """

        return await self._fetchall(
            query,
            params={
                "client": self.client,
                "start_date": params["start_date"],
                "end_date": params["end_date"]
            }
        )

    async def get_realtime_kim_mho(self) -> List[Dict[str, Any]]:
        query = f"""
        {self._get_base_kim_mho_query()}
        WHERE
            kmho.updated_at >= NOW() - INTERVAL 1 YEAR;
        """
        return await self._fetchall(query, {"client": self.client})

    #File
    async def get_files(self, params: FileParams) -> List[Dict[str, Any]]:
        
        query = f"""
        SELECT
        :client as client,
        f.id as file_id,
        f.original_name,
        f.generated_name,
        f.duration,
        f.status,
        f.created_at,
        JSON_OBJECT(
            'id', o.id,
            'name', o.name
        ) AS organization,
        JSON_OBJECT(
            'id', c.id,
            'name', c.name
        ) AS company,
        JSON_OBJECT(
            'id', w.id,
            'name', w.name
        ) AS workstation,
        JSON_OBJECT(
            'id', u.id,
            'name', u.name
        ) AS user
        FROM files f
        LEFT JOIN workstations w ON f.workstation_id = w.id
        INNER JOIN organizations o ON f.organization_id = o.id 
        INNER JOIN companies c ON f.company_id = c.id
        LEFT JOIN users u ON f.user_id = u.id
        WHERE f.created_at >= :start_date
        AND f.created_at <= :end_date
        """
        
        result = await self._fetchall(query, {
            "client": self.client,
            "start_date": params["start_date"],
            "end_date": params["end_date"]
        })
        return result
    
    async def get_files_realtime(self) -> List[Dict[str, Any]]:
        query = f"""
        SELECT
        f.organization_id,
		f.company_id,
		f.workstation_id,
        :client as client,
        JSON_OBJECT('id', ANY_VALUE(o.id), 'name', ANY_VALUE(o.name)) AS organization,
        JSON_OBJECT('id', ANY_VALUE(c.id), 'name', ANY_VALUE(c.name)) AS company,
        CASE 
                WHEN ANY_VALUE(w.id) IS NULL THEN NULL
                ELSE JSON_OBJECT('id', ANY_VALUE(w.id), 'name', ANY_VALUE(w.name))
            END AS workstation,
        COUNT(DISTINCT f.id) AS total_files,
        CASE
            WHEN SUM((atr.id IS NOT NULL)
                        OR (crr.id IS NOT NULL)
                        OR (kmr.id IS NOT NULL)
                        OR (kppr.id IS NOT NULL)) > 0 THEN 1
            ELSE 0
        END AS has_report
        FROM files f
        INNER JOIN organizations o ON f.organization_id = o.id
        INNER JOIN companies c ON c.organization_id = o.id
        LEFT JOIN workstations w ON f.workstation_id = w.id
        LEFT JOIN angle_time_reports atr ON atr.file_id = f.id
        LEFT JOIN custom_report_results crr ON crr.file_id = f.id
        LEFT JOIN kim_mho_reports kmr ON kmr.file_id = f.id
        LEFT JOIN kim_push_pull_reports kppr ON kppr.file_id = f.id
        WHERE f.is_active = 1
        GROUP BY f.organization_id, f.company_id, f.workstation_id
        """
        return await self._fetchall(query, {
            "client": self.client
        })