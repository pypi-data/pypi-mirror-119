REPORT_DESIGNER = {};


// region Элементы


class RdBaseElement {
    /**
     * Базовый класс элемента
     */

    constructor(container) {
        // Контейнер компонента
        this.container = $(container);

        // Наименование компонента
        this.name = this.container.data('name');
    }

    set_trigger(key, args) {
        /**
         * Установка триггера
         */
        key = [
            this.constructor.name.split(/(?=[A-Z])/).map(v => v.toLowerCase()).join('_'),
            key
        ].join(':');
        args = args ? args : [];
        this.container.trigger(key, new Array(...[this.container, ...args]));
    }
}


class RdBaseAjaxContent extends RdBaseElement {
    /**
     * Базовый класс ajax-контента
     */

    constructor(container) {
        super(container)
        // URL для загрузки содержимого
        this.url = this.container.data('url');

        // Автоматическая загрузка
        this.auto_start = rd_utils.str_to_bool(this.container.data('auto-start'));
    }

    post_init() {
        /**
         * Действия после инициализации
         */
        if (this.url && this.auto_start) {
            this.loading();
        }
    }

    loading(url, container) {
        /**
         * Загрузка контента
         */
        let element = this;

        // URL для загрузки
        url = url === undefined ? this.url : url;

        // Контейнер для загрузки
        container = container === undefined ? this.container : container;

        // Триггер перед загрузкой контента
        element.set_trigger('preloading');

        // Загрузка контента
        $.when(rd_utils.ajax_get_request(url))
            .then(function (data) {
                container.html(data['html']);
                rd_init.init_elements(container);
                return Promise.all([data]);
            }).then(function (data) {
                // Триггер после загрузки контента
                element.set_trigger('loaded', data);
            });
    }
}


class RdAjaxContent extends RdBaseAjaxContent {
    /**
     * Ajax-контент
     */

    constructor(container) {
        super(container)

        this.post_init();
    }
}


class RdDynamicList extends RdBaseAjaxContent {
    /**
     * Динамический список
     */

    constructor(container) {
        super(container)

        this.post_init();
    }

    post_init() {
        super.post_init();

        // Загрузка контента
        this.loading_content();

        // События фильтрации
        this.bind_filter_event();
    }

    loading_content() {
        /**
         * Загрузка контента
         */
        this.apply_filter();
        this.bind_paginate_event();
    }

    // region Фильтрация

    bind_filter_event() {
        /**
         * Отслеживание фильтрации
         */
        let dynamic_content = this;

        // Функция вызова фильтрации
        const filter_function = (e) => {
            e.preventDefault();
            dynamic_content.set_trigger('filter:updated', [dynamic_content, e.target]);
            dynamic_content.apply_filter();
        };

        // Прослушивание фильтров
        let filter_container =  $(this.container).find('.js-rd-dynamic-content-filters');
        filter_container.on('change', 'input,select', filter_function);

        // Прослушивание текстовых фильтров
        filter_container.on('keyup', 'input[type="text"]', filter_function);

        // Прослушивание отчистки фильтров
        $(filter_container).on('click', '.js-rd-filters_clear', function (e) {
            /**
             * Кнопка отчистки фильтров
             */
            e.preventDefault();
            dynamic_content.apply_filter_clear();
        });
    }

    apply_filter_clear() {
        /**
         * Действие отчистки фильтра
         */
        let form = $($(this.container).find('.js-rd-dynamic-content-filters').find('form'));
        form[0].reset();
        rd_init.init_elements(form);
        form.find('input,select').trigger('change');
    }

    apply_filter(query) {
        /**
         * Применение фильтров
         */
        // Контейнер с даннными
        let ajax_content = rd_utils.get_from_rd_store('ajax_contents', this.name);

        // URL с параметрами поиска
        let url = `${ajax_content.url}?${query ? query : this.get_content_url_query()}`;

        // Загрузка ajax-content
        ajax_content.loading(url);
    }

    // endregion Фильтрация

    // region Пагинация

    bind_paginate_event() {
        /**
         * Отслеживание пагинации
         */
        let dynamic_content = this;

        // Функция вызова фильтрации
        const paginate_function = (e) => {
            e.preventDefault();
            dynamic_content.set_trigger('paginate:updated', [dynamic_content, e.target]);
            dynamic_content.apply_paginate(e.currentTarget);
        };

        // Прослушивание фильтров
        $(this.container).on(
            'click',
            '.js-rd-dynamic-content-pagination a.js-pagination-page',
            paginate_function
        );

        // Прослушивание фильтров
        $(this.container).on(
            'change',
            '.js-rd-dynamic-content-pagination select.js-pagination-count',
            paginate_function
        );
    }

    apply_paginate(target) {
        /**
         * Применение пагинации
         */
        // Контейнер с даннными
        let ajax_content = rd_utils.get_from_rd_store('ajax_contents', this.name);

        // URL с параметрами поиска
        let value = $(target).val() || $(target).data('value');
        let url = `${ajax_content.url}?${this.get_content_url_query()}&${$(target).data('key')}=${value}`;

        // Создание прелоадера
        ajax_content.loading(url);
    }

    // endregion Пагинация

    get_content_url_query() {
        /**
         * Получение параметров URL для фильтрации
         */
        // Виджеты для сериализации значений
        let widgets = ['input', 'select'];

        // Строка поиска
        return $(this.container).find(`.js-rd-dynamic-content-filters ${widgets.join()}`).serialize();
    }
}


// endregion Элементы


// region Функции


const rd_utils =  {
    /**
     * Вспомогательные функции
     */

    // region Вспомогательные функции

    str_to_bool: function(str) {
        /**
        Перевод из строки в булево значение
         */
        if (typeof str === 'boolean') { return str }
        if (typeof str !== 'string') { return false }
        return String(str).toLowerCase().trim() === 'true';
    },

    add_to_rd_store: function (key, obj) {
        /**
         * Добавление элемента в хранилище конструктора
         */
        if (!REPORT_DESIGNER.hasOwnProperty(key)) {
            REPORT_DESIGNER[key] = [];
        }
        REPORT_DESIGNER[key].push(obj);
    },

    get_from_rd_store(key, name) {
        /**
         * Поиск по наименованию в хранилизе конструктора
         */
        return REPORT_DESIGNER[key].find(obj => obj.name === name);
    },

    // endregion Вспомогательные функции

    // region Ajax запросы

    ajax_request: function(url, type, data) {
        /**
         * Ajax запрос
         */
        let ajax_data = {
            url: url,
            type: type,
            dataType: 'json',
            async: 'true',
        };

        let csrftoken = $('[name=csrfmiddlewaretoken]').val();
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/.test(type.toUpperCase()) && !this.crossDomain) {
            data = data === undefined ? {} : data;
            if (!data.hasOwnProperty('csrfmiddlewaretoken')) {
                data['csrfmiddlewaretoken'] = csrftoken;
            }
            ajax_data['data'] = data;
            ajax_data['beforeSend'] = function(xhr, settings) { xhr.setRequestHeader("X-CSRFToken", csrftoken); }
        }
        return $.ajax(ajax_data);
    },

    ajax_get_request: function (url) {
        /**
         * Ajax GET запрос
         */
        return rd_utils.ajax_request(url, 'GET');
    },

    ajax_post_request: function (url, data) {
        /**
         * Ajax POST запрос
         */
        return rd_utils.ajax_request(url, 'POST', data);
    },

    // endregion Ajax запросы

    // region Модальные окна

    ajax_open_modal_form(url, container, modal_lg) {
        /**
         * Заггрузка и открытие модальной формы
         */
        // Получение контейнера модального окна
        container = container === undefined ? $('#report-designer-modal') : container;

        var dfd = new $.Deferred();
        $.when(rd_utils.ajax_get_request(url))
            .then(function(data) {
                container.toggleClass('modal-lg', modal_lg);
                container.find('.modal-content').html(data['html']);
                rd_init.init_elements(container);
                container.modal('show');
                dfd.resolve(data);
            });
        return dfd.promise();
    }

    // endregion Модальные окна
}


const rd_init = {
    /**
     * Инициализация компонентов
     */

    init_elements: function(container) {
        /**
         * Инициализация элементов
         */
        rd_init.init_ajax_contents(container);
        rd_init.init_dynamic_list(container);
        rd_init.init_select2(container);
    },

    init_ajax_contents: function (container) {
        /**
         * Инициализация RdAjaxContent
         */
        $(container).find('.js-rd-ajax-content').each(function (key, value) {
            let ajax_content = new RdAjaxContent($(value));
            rd_utils.add_to_rd_store('ajax_contents', ajax_content)
        });
    },

    init_dynamic_list: function (container) {
        /**
         * Инициализация RdDynamicList
         */
        $(container).find('.js-rd-dynamic-content').each(function (key, value) {
            let dynamic_content = new RdDynamicList($(value));
            rd_utils.add_to_rd_store('dynamic_contents', dynamic_content)
        });
    },

    init_select2: function(container) {
        /**
         * Инициализация Select2
         */
        // Инициализация выпадающих списков без поиска
        container.find('select').djangoSelect2({
            language: 'ru',
            minimumResultsForSearch: 1,
            width: '100%',
        });
    }
}


function report_designer() {
    /**
     * Конструктор отчетов
     */

    $(document).on('click', '.js-rd-ajax-load-modal-btn', function (e) {
        /**
         * Загрузка модального окна по кнопке
         */
        e.preventDefault();
        rd_utils.ajax_open_modal_form(
            $(this).attr('href'),
            undefined,
            rd_utils.str_to_bool($(this).data('modal-lg'))
        )
    });

    $(document).on('submit', '.js-rd-ajax-form', function (e) {
        /**
         * Отправка ajax формы
         */
        e.preventDefault();

        let form = $(this);
        let container = form.parent();

        // Параметры формы и отправка
        $.when(rd_utils.ajax_post_request(form.attr('action'), form.serializeArray()))
            .then(function (data) {
                let success = data['success'];
                let html = data['html'];

                if (!success) {
                    container.html(html);
                    rd_init.init_elements(container);
                } else {
                    let modal = container.closest('#report-designer-modal');
                    if (modal) {
                        modal.modal('hide');
                    }
                    form.trigger('rd_modal_form:success', data);
                }
            });
    });

    $(document).on('rd_modal_form:success', '.js-rd-ajax-form-create', function (e, data) {
        /**
         * Действия после успешного сохранения ajax-формы
         */
        if (data['redirect_url']) {
            /*
            Перенаправление на указанный URL
             */
            window.location.replace(data['redirect_url']);
        } else if (data['dependent_key'] && data['dependent_name']) {
            /*
            Действия с зависимыми объектами
             */
            let dependent_key = data['dependent_key'];
            let dependent_name = data['dependent_name'];

            let element = rd_utils.get_from_rd_store(dependent_key, dependent_name);
            switch (dependent_key) {
                case 'dynamic_contents':
                    // Чистка фильтров вызовет перезагрузку списка
                    element.apply_filter_clear();
            }
        }

    });
}

// endregion Функции

$(document).ready(function () {
    if(document.getElementById('report-designer')){
        rd_init.init_elements($('#report-designer'));
        report_designer();
    }
});




