package com.hubert.notesmanager.dal;

import java.util.List;

import com.hubert.notesmanager.dal.orm.ClauseEntity;
import com.hubert.notesmanager.data.*;

public interface IDataProvider {
	List<CategoryItem> getCategories();
	List<ClauseEntity> getTiaoWens();
}
