CREATE TABLE users (
    telegram_id BIGINT PRIMARY KEY UNIQUE NOT NULL,
    username TEXT,
    first_name TEXT NOT NULL,
    last_name TEXT,
    registered_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE chats (
    telegram_chat_id BIGINT PRIMARY KEY UNIQUE NOT NULL,
    title TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE users_chats (
    user_id BIGINT REFERENCES users(telegram_id) ON DELETE CASCADE,
    chat_id BIGINT REFERENCES chats(telegram_chat_id) ON DELETE CASCADE,
    PRIMARY KEY (user_id, chat_id)
);
