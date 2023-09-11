import BreadCrumbs from '../BreadCrumbs';
import { useSelector, useDispatch } from 'react-redux';
import {
	openIsAddThemeModalOpen,
	selectAppThemeConfigurationData,
	selectRerenderPage,
	setAppThemeConfigurationData,
} from '../../slice';

import { ReactComponent as AddThemeIcon } from '../../../../assets/images/svg/add-theme-icon.svg';
import AddThemeModal from '../Models/AddThemeModal';
import EachTheme from './EachTheme';
import useApi from '../../../../hooks/useApi';
import { useEffect } from 'react';
import EditThemeModal from '../Models/EditThemeModal';
import { useParams } from 'react-router-dom';

export default function AppThemeConfiguration() {
	let { appId } = useParams();
	const rerenderPage = useSelector(selectRerenderPage);

	const appThemeConfigurationData = useSelector(
		selectAppThemeConfigurationData
	);

	const dispatch = useDispatch();

	const handleAddTheme = () => {
		dispatch(openIsAddThemeModalOpen());
	};

	function updateAppConfigurationData(value) {
		dispatch(setAppThemeConfigurationData(value));
	}

	const triggerApi = useApi();

	useEffect(() => {
		const makeApiCall = async () => {
			const { response, success } = await triggerApi({
				url: `/api/v1/apps/${appId}/themes/`,
				type: 'GET',
				loader: true,
			});
			if (success && response) {
				updateAppConfigurationData(response);
			}
		};

		makeApiCall();
	}, [rerenderPage]);

	return (
		<>
			<div className="flex grow flex-col gap-[40px]">
				<div className="flex items-center justify-between py-[12px] pl-[40px] pr-[48px]">
					<BreadCrumbs />{' '}
					<button
						type="button"
						onClick={handleAddTheme}
						className="flex gap-[8px] rounded-[4px] bg-primary px-[16px] py-[7px]"
					>
						<span className="font-lato text-[14px] font-bold leading-[20px] text-[#FFFFFF]">
							Add Theme
						</span>
						<AddThemeIcon />
					</button>
				</div>
				<div className="flex grow flex-col gap-[20px] pl-[40px] pr-[48px]">
					<div className="flex items-end gap-[24px]">
						<h3 className="font-source-sans-pro text-[22px] font-semibold leading-[28px] text-[#000000]">
							App Name
						</h3>
					</div>
					<div className="complete-hidden-scroll-style grid grid-cols-1 items-stretch justify-start gap-[26px] overflow-y-auto pb-[29px] sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-4 2xl:grid-cols-5">
						{appThemeConfigurationData?.themes?.map((eachTheme) => {
							return <EachTheme key={eachTheme?.id} data={eachTheme} />;
						})}
					</div>
				</div>
			</div>
			<AddThemeModal />
			<EditThemeModal />
		</>
	);
}
